#!/usr/bin/env bash

export ENVIRONMENT=test

echo "
[run]
omit =
    */base.py
    main/__init__.py
    main/config/*
    tests/*
" > ./.coveragerc

rm -rf ./cov_html/
py.test tests --cov=main --cov-report term-missing --cov-report html:cov_html
open cov_html/index.html