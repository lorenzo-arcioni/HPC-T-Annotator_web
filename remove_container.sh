#!/bin/bash

docker stop flask
docker stop nginx

docker remove flask
docker remove nginx
