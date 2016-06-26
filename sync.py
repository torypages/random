#!/usr/bin/env python3
from os.path import expanduser
from os.path import join
from os.path import exists
from os.path import isdir
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import argparse
import subprocess
import time
import yaml
import yaml

# Thanks to https://www.michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
# for the example.

def run_rsync(src_path, full_remote_path, recursive, host, delete=False):
    recursive = '-r' if recursive else ''
    full_remote_path += '/' if not full_remote_path[-1] == '/' else ''
    if delete:
        while not exists(src_path):
            src_path_tmp = src_path.rsplit('/', 1)[0]
            if src_path_tmp == src_path:
                raise Exception("watching dir is gone")
            src_path = src_path_tmp
    elif not delete and not exists(src_path):
        print("Deleted, skipping")
        return
    # only way dir can happen is on delete
    src_path += '/' if isdir(src_path) else ''
    cmd = ['rsync', recursive, src_path, '{}:{}'.format(host, full_remote_path)]
    if delete:
        cmd.append('--delete')
    cmd = [i for i in cmd if i]
    print(" ".join(cmd))
    x = subprocess.check_output(cmd)
    print(x)

class Watcher:
    watch_dir = None
    host = None
    remote_base = None
    args = None

    def __init__(self, watch_dir, host, remote_base, args):
        self.watch_dir = watch_dir
        self.host = host
        self.remote_base = remote_base
        self.observer = Observer()
        self.args = args

        print("Performing initial sync")
        run_rsync(watch_dir, '{}/{}'.format(self.remote_base, watch_dir),
                  recursive=True, host=self.host, delete=self.args.delete)
        print("Finished initial sync")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            pass
            #print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            pass
            #print("Received modified event - %s." % event.src_path)

        remote_path = event.src_path.rsplit('/', 1)[0]
        #print(remote_path)
        full_remote_path = '{}/{}'.format(remote_base, remote_path)
        print('frp', full_remote_path)
        run_rsync(event.src_path, full_remote_path,
                  recursive=True, host=host, delete=args.delete)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    parser.add_argument("--config-path", required=False)
    parser.add_argument("--delete", default=False, action='store_true')
    args = parser.parse_args()

    if args.config_path:
        conf_path = args.config_path
    else:
        conf_path = join(expanduser('~'), '.config', 'synced.yaml')

    #host = 'tmclust'
    #remote_base = '~/CodeSynced'
    conf = yaml.load(open(conf_path, 'r'))
    host = conf['host']
    remote_base = conf['remote_base']
    

    watch_dir = '{}'.format(args.dir.rsplit('/', 1)[0])
    w = Watcher(watch_dir=watch_dir, host=host,
                remote_base=remote_base, args=args)
    w.run()
