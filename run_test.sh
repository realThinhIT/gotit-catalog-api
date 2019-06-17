#!/usr/bin/env bash

export ENVIRONMENT=test
export FLASK_ENV=test

py.test tests --cov=main