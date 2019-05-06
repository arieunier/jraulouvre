APPNAME=$1

export PYTHONPATH=.:./libs/:./appsrc/:./pyutils
export DATABASE_URL=`heroku config:get DATABASE_URL --app $APPNAME`
export LOGDNA_KEY=`heroku config:get LOGDNA_KEY --app $APPNAME`
export REDIS_URL=`heroku config:get REDIS_URL --app $APPNAME`
export SENDGRID_API_KEY=`heroku config:get SENDGRID_API_KEY --app $APPNAME`
export LOG_LEVEL=debug
