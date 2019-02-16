web: cp newrelic.ini.template newrelic.ini; newrelic-admin generate-config $NEW_RELIC_LICENSE_KEY newrelic.ini; export PYTHONPATH=.:./libs:./appsrc; env; newrelic-admin run-program gunicorn --workers=8  --backlog=1024 run:app


