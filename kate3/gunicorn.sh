#!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/kate3.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  USER=smizell
  GROUP=smizell
  cd /web/projects/kate3base
  source bin/activate
  cd /web/projects/kate3base/src/kate3
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec /web/projects/kate3base/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
