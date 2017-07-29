# Creating a Jupyter Notebook server user service
System: Ubuntu 16.04

Create file `~/.config/systemd/user/jupyter.service`

```
[Unit]
Description=Jupyter Notebook

[Service]
Type=simple
ExecStart=/home/USER/Python/envs/jupyter_server/bin/jupyter-notebook \
          --config=/home/USER/.jupyter/jupyter_notebook_config.py
WorkingDirectory=/home/f/
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```
systemctl --user enable jupyter.service
systemctl start --user jupyter.service
```


This is how you can get a persistent Jupyter Notebook Server running under your
user using SystemD and Ubuntu 16.04 Linux.

If your system actually had multiple users on the system you would have to do
something that will dynamically select ports or something of that sort.

Additionally I think you can use `@` in the service name to include the
username in the service. I'm not sure, but, I am the sole user of this
system, so, I don't care.

I haven't actually restarted my system yet, I don't know for a fact that it
will launch on reboot.

If you modify your SystemD unit file you have to run 
`systemctl --user daemon-reload` in order to reload it.


