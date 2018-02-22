#!/bin/bash
export GF_CONFIG_CLASS=config.DebugConfig
export FLASK_DEBUG=1
gunicorn -b 0.0.0.0:8000 app:app
