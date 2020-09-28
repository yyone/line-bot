#!/bin/sh
sudo kill -9 `cat /var/www/flask/tmp/uwsgi.pid`
