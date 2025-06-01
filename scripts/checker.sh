#!/usr/bin/sh
# run from package root
mypy --sqlite-cache --warn-unreachable --pretty --strict -p quarryforge
