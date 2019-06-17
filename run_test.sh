#!/usr/bin/env bash

export ENVIRONMENT=test
export FLASK_ENV=test

echo "
[run]
omit =
    */base.py
    main/__init__.py
    main/config/*
    tests/*
" > ./.coveragerc

py.test tests --cov=main