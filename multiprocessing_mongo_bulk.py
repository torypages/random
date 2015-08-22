#!/bin/env python2
from pymongo import MongoClient
import multiprocessing
import time
import logging

# Room for improvement: handling of errors and empty mongo bulk executes.
# Be smarter about what it means to max out memory.
#  Doc count isn't the best one can do.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, host, port, db, collection):
        self.coll = MongoClient(host, port)[db][collection]
        self.mongo_bulk = self.coll.initialize_unordered_bulk_op()
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        count = 0

        def execute_mongo_bulk():
            try:
                self.mongo_bulk.execute()
                self.mongo_bulk = self.coll.initialize_unordered_bulk_op()
                logger.info("executing mongo bulk")
            except Exception, e:
                logger.info(e)

        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break

            next_task(self.mongo_bulk)
            if count % 1000 == 0:
                execute_mongo_bulk()
            self.task_queue.task_done()

        execute_mongo_bulk()
        return


class Task(object):
    def __init__(self, mongo_doc):
        self.mongo_doc = mongo_doc

    def __call__(self, mongo_bulk):
        # Ideally you do something expensive here, otherwise there is no point of multiprocessing
        random_num = self.mongo_doc['num'] / 3.14
        date_str = str(self.mongo_doc['date'])
        concat = "{}{}".format(str(random_num), date_str)
        docid = self.mongo_doc['_id']
        mongo_bulk.find({'_id': docid}).upsert().update({'$set': {'concat': concat}})

if __name__ == '__main__':
    dbhost = '192.168.1.6'
    dbport = 27017
    dbstr = 'test'
    colstr = 'random_numbers'

    tasks = multiprocessing.JoinableQueue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print("Creating {} consumers".format(num_consumers))
    consumers = [Consumer(tasks, dbhost, dbport, dbstr, colstr + '_out')
                 for i in xrange(num_consumers)]

    for w in consumers:
        w.start()

    # Create jobs
    random_numbers = MongoClient(dbhost, dbport)[dbstr][colstr]
    for mongo_doc in random_numbers.find():
        tasks.put(Task(mongo_doc))
        while tasks.qsize() > 1000000:
            # I don't want too many mongo docs sitting in memory
            logger.info("Queue size maxed, waiting.")
            time.sleep(1)

    logger.info("Broadcasting poison pill")
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    logger.info("Waiting for processes to finish.")
    # Wait for all of the tasks to finish
    tasks.join()
    logger.info("All done!")

