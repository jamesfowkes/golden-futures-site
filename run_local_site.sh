#!/bin/bash
export GF_CONFIG_CLASS=config.DebugConfig
export FLASK_DEBUG=1
python3 runner.py --debug
