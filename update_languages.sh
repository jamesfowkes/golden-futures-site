pybabel extract -F babel.cfg -o messages.pot app
pybabel update -i messages.pot -d app/translations