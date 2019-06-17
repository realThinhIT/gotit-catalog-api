#!/usr/bin/env bash

export ENVIRONMENT=test
export FLASK_ENV=test

echo "
[run]
omit =
    main/__init__.py
    main/config/*
    tests/*
" > ./.coveragerc

py.test tests --cov=main