#!/bin/sh

for u in `cat /etc/passwd | cut -d":" -f1`;
    do crontab -l -u $u;
done