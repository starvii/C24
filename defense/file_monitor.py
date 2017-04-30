#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue, Manager
from threading import Thread
from shutil import copy2, rmtree
import signal
import os
import sys
import time
from logger import get_logger
from pyinotify import ProcessEvent, WatchManager, Notifier, IN_CREATE, IN_MODIFY, IN_DELETE


"""
    the daemon process prints and logs message from queue.
    
    the 1st process (most important) compares datetime of the file and backup to discover which file is changed, then recovers it from 
    backup. 
    
    the 2nd process uses multi threads to monitor file change.
    the 1st thread uses pyinotify to monitor file events. 
    (but sometime it would not work. I don't know why. Maybe pyinotify just works in the level of Shell.)
    It just monitors, won't recover the file.
    the 2nd thread computes file fingerprint(MD5) to discovery which file is changed.
"""

monitor_dirs = {}
exclude_dirs = set(())  # monitor_dir: backup_dir
delay = 0


msg_q = Queue()


def onerror(err):
    # TODO: add process name
    msg_q.put_nowait(err)


def get_mon_bak_base(path):
    for d in monitor_dirs.keys():
        if path.startswith(d):
            return d, monitor_dirs[d]


def is_exclude(path):
    for d in exclude_dirs:
        if path.startswith(d):
            return 1
    return 0


def compare_by_time(mon_path, bak_path):
    """
    compare path state
    :param mon_path: 
    :param bak_path: 
    :return: 
        0: no problem.
        1: mon_path exists but bak_path not exists.
        2: mon_path and bak_path both exist, but creating timestamp and modifying timestamp are different.
    """
    if os.path.exists(mon_path) and not os.path.exists(bak_path):
        return 1
    if os.path.exists(mon_path) and os.path.exists(bak_path):
        mon_ct = os.path.getctime(mon_path)
        mon_mt = os.path.getmtime(mon_path)
        bak_ct = os.path.getctime(bak_path)
        bak_mt = os.path.getmtime(bak_path)
        if mon_ct != bak_ct or mon_mt != bak_mt:
            return 2
    return 0


def monitor_by_time():
    while 1:
        for d in monitor_dirs:
            for t in os.walk(d, onerror=onerror, followlinks=True):
                mon_path = t[0]
                if os.path.isfile(mon_path):
                    mon_base, bak_base = get_mon_bak_base(mon_path)
                    bak_path = mon_path.replace(mon_base, bak_base)
                    r = compare_by_time(mon_path, bak_path)
                    if 0 == r:
                        continue
                    elif 1 == r:
                        rmtree(mon_path, ignore_errors=False, onerror=onerror)
                    elif 2 == r:
                        copy2(bak_path, mon_path)
                elif os.path.isdir(mon_path):
                    pass
                else:
                    # maybe some links or mounts?
                    pass
        time.sleep(delay)


def monitor_aide():
    pass


def monitor_by_pyinotify():
    # from pyinotify import
    pass


def monitor_by_fingerprint():
    pass


def main():
    # start processes
    proc_main = Process(target=monitor_by_time)
    proc_main.daemon = True
    proc_main.start()
    proc_aide = Process(target=monitor_aide)
    proc_aide.daemon = True
    proc_aide.start()
    # reading message from queue
    log = get_logger('file_monitor')
    try:
        while 1:
            msg = msg_q.get(block=True)
            log.info(msg)
    except KeyboardInterrupt:
        print 'CTRL + C were pressed.'
        proc_main.terminate()
        proc_aide.terminate()
        sys.exit(0)


if __name__ == '__main__':
    main()
