#!/bin/bash

ASGI_HOST=${WSGI_HOST:="0.0.0.0"}
ASGI_PORT=8000
ASGI_WORKERS=${WSGI_WORKERS:=1}
WORKER_NUM_PROCESSES=${WORKER_NUM_PROCESSES:=1}

RUN_SERVER=${RUN_SERVER:="FALSE"}
RUN_CELERY=${RUN_CELERY:="FALSE"}


if [ $RUN_SERVER = "TRUE" ]; then
  service nginx restart
  uvicorn --workers $ASGI_WORKERS --host $ASGI_HOST --port $ASGI_PORT config.asgi:application
elif [ $RUN_CELERY = "TRUE" ]; then
  service nginx stop
  celery -A config worker
else
  echo "You have to set RUN_CELERY or RUN_SERVER to TRUE"
  echo "Exiting"
fi
