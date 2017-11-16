export GF_CONFIG_CLASS=config.DebugConfig
export FLASK_DEBUG=1
#/home/james/.virtualenvs/golden-futures/bin/gunicorn -b 0.0.0.0:8000 app:app
python3 runner.py --debug
