#!/bin/sh

ps -ef | grep -E 'curl|wget' | grep -v -E 'root|grep' | awk '{print $2}' | xargs kill -9 2 > /dev/null
