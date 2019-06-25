#!/bin/bash

sleep 10
source /root/.local/share/virtualenvs/flight-booking-*/bin/activate
echo "<<<<<<<<<< Export LANG to the Env>>>>>>>>>>"

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
sleep 20
# Run database migrations
flask db upgrade

sleep 20
echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
echo " "

sleep 5
echo " "
echo "<<<<<<<<<<<<<<<<<<<< START Celery >>>>>>>>>>>>>>>>>>>>>>>>"

# start Celery worker
celery worker -A celery_worker.celery_app --loglevel=info &

# start celery beat
celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info &

sleep 10
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"
# Start the API with gunicorn
gunicorn --access-logfile '-' --workers 2 manage:app -b 0.0.0.0:5000
