#!/usr/bin/sh
# run from package root
coverage run -m pytest tests
coverage html
