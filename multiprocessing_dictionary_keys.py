from collections import defaultdict
import multiprocessing
from pprint import pprint
import hashlib
import random
import time


"""
* I have an existing set of data keyed by usernames.
* I have a new set of ungrouped data that contains usernames. Usernames
can repeat in this data, and won't be grouped.
* The new data can contain usernames that don't exist in the
existing data.
* I want to combine the new data with the existing data in arbitrary
ways. In this demo I will just be doing a += 1 but this is a simplification.
* The existing way to do this is looping through the new data and
updating the existing data accordingly.
* I want to do this with multiprocessing but I have a large dictionary
that I need to work with.
* All processing would need access to this dictionary but sharing a
dictionary across processes is lame.
* Further, if multiple processes were to access the same section
of the dictionary at the same time we would be in a bad place.
* The key thing is to avoid this, there are a few ways of accomplishing this
the method I have chosen is a bit overkill, but it is fairly simple.
* It would appear that storage of data and processing data pertaining
to a user must only ever occur on a single process.
* I need a way to distribute the work. I could randomly assign usernames
to processes and then forever use that process for the username, but then
I would have to store all this information.
* A way to store less data would be to hash usernames to something simple
and user that small hash to assign ranomly to processes.

* Some other thoughts:
* I could just write to a shared data store and use Optimistic
Concurrently Control
https://www.elastic.co/guide/en/elasticsearch/
 guide/current/optimistic-concurrency-control.html
to deal with the fact that there could be a collision while accessing the
shared datastore.
* Perhaps I could have a special queue for a username. Most of the time
the queue would come up and end very quickly, only processing a single
item, but in the case that a username came up twice in quick succession
then multiple items could end up in the queue.
"""


# I will aggregate and count the characters in a textfile as a way
# to demonstrate.


# Here is how the problem could be solved without multiprocessing.
def single_process(word_list):
    data = defaultdict(int)
    for key in word_list:
        current_value = data[key]
        new_value = current_value + 1
        # time.sleep(.01)
        data[key] = new_value
    pprint(data)


# Will using a hashing algorithm allow me to evenly distribute work
# amongst workers?
def test_distribution(word_list):
    for key in word_list:
        d_key = my_hash(key)
        # results in 6 values for 6 consumers
        d[d_key] = random.randint(0, 5)
    pprint(d)

    test_d = defaultdict(int)
    for k, v in d.items():
        test_d[v] += 1

    pprint(test_d)
    # defaultdict(<class 'int'>, {0: 12, 1: 11, 2: 15, 3: 14, 4: 15, 5: 15})
    # Distribution is great.


# From here I will solve the task with multiprocessing.
class Consumer(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.count_dict = defaultdict(int)

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            next_task(self.count_dict)
            self.task_queue.task_done()
        pprint(self.count_dict)
        return


class Task(object):
    def __init__(self, some_word):
        self.some_word = some_word

    def __call__(self, count_dict):
        count_dict[self.some_word] += 1
        time.sleep(.01)


def multi_process(word_list):
    num_consumers = 6
    queues = [multiprocessing.JoinableQueue() for i in range(num_consumers)]
    consumers = [Consumer(queues[i]) for i in range(num_consumers)]
    queue_ids = {}
    for consumer in consumers:
        consumer.start()

    for key in word_list:
        queue_key = my_hash(key)
        queue_index = None
        if queue_key not in queue_ids:
            queue_index = random.randint(0, num_consumers - 1)
            queue_ids[queue_key] = queue_index
        else:
            queue_index = queue_ids[queue_key]
        queues[queue_index].put(Task(key))

    for queue in queues:
        queue.put(None)

    for queue in queues:
        queue.join()


def my_hash(x):
    x = x.encode('utf-8')
    return hashlib.md5(x).hexdigest()[:2]


def get_queue_index(x):
    h = my_hash(x)


if __name__ == '__main__':
    d = defaultdict(int)
    word_list = [i for i in open('multiprocessing_dictionary_keys_data.txt', 'r').read()]
    start = time.time()
    # test_distribution(word_list)
    # single_process(word_list[:1000])
    # print('------------------------------------------')
    # multi_process(word_list[:1000])
    end = time.time()
    print(end - start)

