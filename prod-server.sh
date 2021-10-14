#!/bin/bash
export FLASK_ENV=production
gunicorn -w 4 cms.wsgi:app