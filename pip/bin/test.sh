#! /usr/bin/env bash

export PYTHONPATH=src/
pytest --cov --cov-report term-missing
