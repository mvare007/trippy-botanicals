#!/bin/bash
# this script is used to boot a Docker container
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrxying in 5 secs...
    sleep 5
done

if [ "$FLASK_ENV" == "production" ]; then
    exec gunicorn -b :8000 --access-logfile - --error-logfile - trippy:app
fi