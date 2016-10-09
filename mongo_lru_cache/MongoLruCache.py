from collections import OrderedDict
from pymongo import UpdateOne
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mongo-lru-cache')


class StateDict(dict):
    """
    Enable the ability to only write back to mongo when a document has
    been mutated.
    """
    def __init__(self, some_dict):
        self.mutated = False
        super().__init__(some_dict)

    def __setitem__(self, key, value):
        self.mutated = True
        super().__setitem__(key, value)


class MongoLruCache(object):
    def __init__(self, mongo_collection, cache_size):
        self.cache = OrderedDict()
        self.collection = mongo_collection
        self.cache_size = cache_size
        self.cache_key_signature = None

    @staticmethod
    def tupels_tuples_to_dict(x):
        """
        Convert the tuples of tuples to a dict, probably for the purposes
        of doing a Mongo lookup / filter
        """
        return {k: v for k, v in x}

    @staticmethod
    def extract_signature(x):
        """
        Extract signature of the key, that is, the fields which are used
        in the Mongo lookup query / filter
        """
        return [k for k, v in x]

    def check_key_signature(self, key):
        """
        Accessing the cache with a different key could lead to unexpected
        results if not extremely careful, so, just ban the practice.
        """
        key_sig = self.extract_signature(key)
        if self.cache_key_signature:
            if not key_sig == self.cache_key_signature:
                raise Exception('Key signature has changed!')
        else:
            self.cache_key_signature = key_sig

    def __getitem__(self, key):
        self.check_key_signature(key)

        query = self.tupels_tuples_to_dict(key)
        if key in self.cache:
            item = self.cache.pop(key)
            self.cache[key] = item
            return item
        else:
            item = self.collection.find_one(query)
            if not item:
                return None
            else:
                item = self.set(key, item)
                return item

    def __setitem__(self, key, value):
        self.check_key_signature(key)
        self.set(key, value, mutated=True)

    # enable use as context manager
    def __enter__(self):
        return self

    # enable use as context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Exiting context manager.")
        self.write_out_cache()

    def set(self, key, val, mutated=False):
        self.check_key_signature(key)
        val = StateDict(val)
        val.mutated = mutated
        if len(self.cache) >= self.cache_size:
            self.pop()
        self.cache[key] = val
        return val

    def pop(self):
        # By popping and removing now it assumes the mongo update will
        # succeed.
        if not len(self.cache):
            return None
        key, val = self.cache.popitem(last=False)
        logger.debug("Popping: {}".format(key))
        if val.mutated:
            logger.debug("Updating one")
            self.collection.update_one(self.tupels_tuples_to_dict(key),
                                       {'$set': val}, upsert=True)

    def write_out_cache(self):
        """
        Upsert all modified docs to Mongo
        """
        logger.debug("Writing out cache.")
        bulk_size = 2
        action_ops = []
        for key, val in self.cache.items():
            if val.mutated:
                action_ops.append(UpdateOne(self.tupels_tuples_to_dict(key),
                                            {'$set': val}, upsert=True))
                if bulk_size >= len(action_ops):
                    self.collection.bulk_write(action_ops)
                    action_ops = []
        if len(action_ops):
            self.collection.bulk_write(action_ops)

    def __contains__(self, key):
        self.check_key_signature(key)
        return key in self.cache

    def __len__(self):
        return len(self.cache)
