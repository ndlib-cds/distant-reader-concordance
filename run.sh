#!/bin/bash

env CONFIG=config.local FLASK_ENV=development FLASK_APP=main.py flask run
