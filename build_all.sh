#!/bin/bash

mkdir -p log/nginx
touch log/nginx/access.log
touch log/nginx/error.log

mkdir -p log/uwsgi
touch log/uwsgi/uwsgi_access.log
touch log/uwsgi/uwsgi_error.log

./clear_log_files.sh

docker compose up --build -d
