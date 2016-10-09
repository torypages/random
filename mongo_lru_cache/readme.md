# MongoLruCache
* This is a class that is meant to facilitate performant random access to data in a Mongo collection.
* Two sort of awkward items to be aware of:
 * You are required to consistently access data using the same key to lookup data or to upsert on.
   * This is not a technical limitation, it is just to keep you from breaking your data.
 * This key must be a tuple of tuples, and a tuple of a tuple has an awkward required comma ((tuple),)
  * (('foo', 'bar'), {'chew', 'dar') is converted to {'foo': 'bar', 'chew': 'dar'} when interacting with Mongo
  * Perhaps instead I should take a list of tuples then convert them.
