#!/bin/sh
#
# kate3     Starts the kate3 Django project
#
# chkconfig:    345 90 90
# description:  kate3 gunicorn script   


ADDRESS='127.0.0.1'
PYTHON="/web/projects/kate3base/bin/python"
GUNICORN="/web/projects/kate3base/bin/gunicorn_django"
PROJECTLOC="/web/projects/kate3base/src/kate3"
VENV_DIR="/web/projects/kate3base"
MANAGELOC="$PROJECTLOC/manage.py"
DEFAULT_ARGS="--workers=3 --daemon --log-file=/var/log/gunicorn/kate3.log --bind=$ADDRESS:"
SOURCE_CMD="source bin/activate"
BASE_CMD="$GUNICORN $DEFAULT_ARGS"

SERVER1_PORT='8000'
SERVER1_PID="/var/run/$SERVER1_PORT.pid"
SERVER2_PORT='8001'
SERVER2_PID="/var/run/$SERVER2_PORT.pid"

start_server () {
  if [ -f $1 ]; then
    #pid exists, check if running
    if [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
       echo "Server already running on ${ADDRESS}:${2}"
       return
    fi
  fi
  cd $VENV_DIR
  $SOURCE_CMD
  cd $PROJECTLOC
  echo "starting ${ADDRESS}:${2}"
  $BASE_CMD$2 --pid=$1
}

restart_server (){
  if [ -f $1 ] && [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
    echo "restarting server ${ADDRESS}:${2}"
    kill -HUP `cat $1`
  else
    if [ -f $1 ]; then
      echo "server ${ADDRESS}:${2} not running"
    else
      echo "No pid file found for server ${ADDRESS}:${2}"
    fi
  fi
}

stop_server (){
  if [ -f $1 ] && [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
    echo "stopping server ${ADDRESS}:${2}"
    kill -9 `cat $1`
    rm $1
  else 
    if [ -f $1 ]; then
      echo "server ${ADDRESS}:${2} not running"
    else
      echo "No pid file found for server ${ADDRESS}:${2}"
    fi
  fi
}

case "$1" in
start)
  start_server $SERVER1_PID $SERVER1_PORT 
  #start_server $SERVER2_PID $SERVER2_PORT
  ;;
stop)
  stop_server $SERVER1_PID $SERVER1_PORT
  #stop_server $SERVER2_PID $SERVER2_PORT
  ;;
restart)
  restart_server $SERVER1_PID $SERVER1_PORT
  #stop_server $SERVER1_PID $SERVER1_PORT
  #sleep 2
  #start_server $SERVER1_PID $SERVER1_PORT
  #sleep 2
  #stop_server $SERVER2_PID $SERVER2_PORT
  #sleep 2
  #start_server $SERVER2_PID $SERVER2_PORT
  ;;
*)
  echo "Usage: $0 { start | stop | restart }"
  ;;
esac

exit 0
