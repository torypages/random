Here is a cool little thing you can do with Systemd. Upon the failure of a service you can run an arbitrary command via another unit file. I thought of this as being useful when running a service in an AWS autoscaling group. For example, if a service were to fail, you could copy the logs somewhere and and then just shutdown the instance. By doing this, the autoscaling group should spin up a new instance hopefully with a functioning service. This came up in the context of services on failing and resulting in instances in the autoscaling group just sitting around doing nothing. Perhaps a bit cleaner, you could emit a custom health check http://docs.aws.amazon.com/autoscaling/latest/userguide/healthcheck.html#as-configure-healthcheck to signal that the instance is unhealthy instead of shutting down.

fail_test.service:
```
[Unit]
Description=Fail Test
OnFailure=fail_action.service

[Service]
Type=simple
ExecStart=/bin/bash -c "while true; do date >> /tmp/fail_test.log; sleep 1; done;"


[Install]
WantedBy=multi-user.target
```

cat fail_action.service
```
[Unit]
Description=Action to do on fail

[Service]
ExecStart=/bin/bash -c "echo 'I failed ' + date > /tmp/i_failed.log"

[Install]
WantedBy=multi-user.target
```
