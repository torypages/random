from MongoLruCache import MongoLruCache
from unittest.mock import MagicMock
import binascii
import logging
import mongomock
import os
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mongo-lru-cache-test')

def bulk_write_hack(*args, **kwargs):
    # bulk_write did not exist in mongomock at the time of writing
    # this is only for my particular situation, nothing else
    assert(not kwargs)
    assert(len(args) == 2)
    coll = args[0]
    updates = args[1]
    for i in updates:
        coll.update_one(i._filter, i._doc, upsert=i._upsert)

mongomock.Collection.bulk_write = bulk_write_hack


class MongoLruCacheTest(unittest.TestCase):
    def rnd(self, x):
        self.unique_rnd += 1
        return binascii.hexlify(os.urandom(x)).decode("utf-8") \
               + str(self.unique_rnd)

    def fill_mock_data(self, collection):
        for i in range(15):
            d = {i:self.rnd(10) for i in "abcdefghij"}
            collection.insert_one(d)

    def setUp(self):
        self.unique_rnd = 0
        self.collection = mongomock.MongoClient()['db']['collection']
        self.fill_mock_data(self.collection)

    def test_cache_after_get(self):
        lru = MongoLruCache(self.collection, 5)
        some_doc = self.collection.find_one()
        some_key = (('a', some_doc['a']),)
        cached_doc = lru[some_key]
        self.assertEqual(len(lru), 1)
        self.assertIn(some_key, lru)

    def test_cache_ejection(self):
        cache_size = 5
        lru = MongoLruCache(self.collection, cache_size)
        db_docs = list(self.collection.find().limit(cache_size + 1))
        for i in db_docs:
            key = (('a', i['a']),)
            logger.debug("Accessing: {}".format(key))
            doc_from_cache = lru[key]
            self.assertIsNotNone(doc_from_cache)

        self.assertNotIn((('a', db_docs[0]['a']),), lru)

        for i in range(1, cache_size - 1):
            self.assertIn((('a', db_docs[i]['a']),), lru)

        self.assertEqual(cache_size, len(lru))

    def test_pop_save(self):
        lru = MongoLruCache(self.collection, 5)
        some_doc = self.collection.find_one()
        some_key = (('a', some_doc['a']),)
        cached_doc = lru[some_key]
        cached_doc['cool'] = "supercoolpeople"
        lru.pop()
        some_update_doc = self.collection.find_one(some_doc)
        self.assertIsNotNone(some_update_doc)
        self.assertEqual(some_update_doc['cool'], 'supercoolpeople')

    def test_write_out_cache(self):
        cache_size = 15
        lru = MongoLruCache(self.collection, cache_size)
        docs = self.collection.find().limit(cache_size)
        keys = [(('a', i['a']),) for i in docs]
        self.assertEqual(cache_size, len(keys))
        for key in keys:
            lru[key]['king'] = 'george'
        lru.write_out_cache()
        for doc in docs:
            r = self.collection.find_one({'a': doc['a']})
            self.assertIn('king', r)
            self.assertEqual(r['king'], 'george')

    def test_context_manager(self):
        with MongoLruCache(self.collection, 5) as lru:
            flag = False
            def t():
                nonlocal flag
                logger.debug("Fake write_out_cache")
                flag = True
                logger.debug("Flag val {}".format(flag))
            lru.write_out_cache = t
        self.assertTrue(flag)


    def test_mutated_single(self):
        """
        Different from test_pop_save because it tests that the write
        does _not_ happen when it is not required.
        """
        cache_size = 2
        lru = MongoLruCache(self.collection, cache_size)
        db_doc = self.collection.find_one()
        self.collection.bulk_write = MagicMock()
        lru.pop()
        self.assertFalse(self.collection.bulk_write.called)

    def test_mutated_write_out(self):
        cache_size = 2
        lru = MongoLruCache(self.collection, cache_size)
        db_doc = self.collection.find_one()
        self.collection.bulk_write = MagicMock()
        lru.write_out_cache()
        self.assertFalse(self.collection.bulk_write.called)

    def test_new_value(self):
        cache_size = 2
        lru = MongoLruCache(self.collection, cache_size)
        key = (("something", "new"),)
        lru[key] = {"super": "duper"}
        self.assertIn(key, lru)
        lru.write_out_cache()
        self.assertTrue(self.collection.find_one({k: v for k, v in key}))
