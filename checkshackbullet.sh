#!/bin/bash
#
# watchdog script for shackbullet
# rather than actually do error handling, just restart it if it dies
# meant to be run every minute in crontab like the following
# * * * * * /path/to/checkshackbullet.sh
ps ax | grep -v grep | grep "python /path/to/shackbullet.py"
case "$?" in
   0)
   /bin/true
   ;;
   1)
   python /path/to/shackbullet.py&
   ;;
esac

exit
