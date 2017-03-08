# Mongo Replication Error

```
2017-03-04T06:59:20.620+0000 E REPL     [repl writer worker 7] Error applying command ({ ts: Timestamp 1488555163000|41, h: 6121498083483076147, v: 2, op: "c", ns: "admin.$cmd", o: { renameCollection: "somedb.collection_temp", to: "somedb.collection", dropTarget: true } }): OplogOperationUnsupported: Applying renameCollection not supported in initial sync: { ts: Timestamp 1488555163000|41, h: 6121498083483076147, v: 2, op: "c", ns: "admin.$cmd", o: { renameCollection: "somedb.collection_temp", to: "somedb.collection", dropTarget: true } }
2017-03-04T06:59:20.620+0000 I -        [repl writer worker 7] Fatal assertion 15915 OplogOperationUnsupported: Applying renameCollection not supported in initial sync: { ts: Timestamp 1488555163000|41, h: 6121498083483076147, v: 2, op: "c", ns: "admin.$cmd", o: { renameCollection: "somedb.collection_temp", to: "somedb.collection", dropTarget: true } }
2017-03-04T06:59:20.620+0000 I -        [repl writer worker 7] 

***aborting after fassert() failure
```

It appears that there was a change in specifically Mongo 3.2.12 that casues this:


```
$~/TorypagesCode/mongo$ git checkout tags/r3.2.12
Previous HEAD position was 009580a... SERVER-25027 Configurable connpool in mongos
HEAD is now at ef3e1bc... SERVER-27125 Arbiters in PV1 vote no if they can see a healthy primary of equal or greater priority to the candidate
$~/TorypagesCode/mongo$ grep "Applying renameCollection not supported in initial sync" * -R
src/mongo/db/repl/oplog.cpp:                          << "Applying renameCollection not supported in initial sync: " << op);
$:~/TorypagesCode/mongo$ 
$:~/TorypagesCode/mongo$ git checkout tags/r3.2.11                                                                                                                                                                                                                              
Previous HEAD position was ef3e1bc... SERVER-27125 Arbiters in PV1 vote no if they can see a healthy primary of equal or greater priority to the candidate
HEAD is now at 009580a... SERVER-25027 Configurable connpool in mongos
$:~/TorypagesCode/mongo$ grep "Applying renameCollection not supported in initial sync" * -R
```

I'm sure there is good reason for this change in terms of maintaining data integrity, but since this is a brand new feature you might be put in a bad place. You could run 3.2.11 to skirt the issue. I'm not sure what later generations have in this regard.
