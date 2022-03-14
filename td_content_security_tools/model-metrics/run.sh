#!/bin/bash

gunicorn --reload server:app \
         -b 0.0.0.0:5001 \
         -w 1
