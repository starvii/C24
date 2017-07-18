#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import re
from collections import deque


# port and process info
# netstat -lntp
# ls -l /proc/{pid}/exe


def port_proc_info():
    o = subprocess.Popen('netstat -lntp', shell=True, stdout=subprocess.PIPE)
    lines = o.stdout.readlines()
    i = 0
    while not lines[i].startswith('Proto'):
        i += 1
    lines = lines[i + 1:]
    lines = map(lambda x: x.strip(), lines)
    r = deque()
    for line in lines:
        l = re.split('\s+', line)
        proto = l[0]
        address_port = l[3]
        pid_exe = ' '.join(l[6:])
        if '/' in pid_exe:
            temp = pid_exe.split('/')
            pid = temp[0]
            o = subprocess.Popen('ls -l /proc/%s/exe' % pid, shell=True, stdout=subprocess.PIPE)
            exe = o.stdout.read().split('->')[1].strip()
            print proto, address_port, pid, exe
            r.append((proto, address_port, pid, exe))
    return r


if __name__ == '__main__':
    port_proc_info()
