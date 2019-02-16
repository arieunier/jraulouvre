APPNAME=$1

export PYTHONPATH=.:./libs/:./appsrc/:./pyutils
export DATABASE_URL=`heroku config:get DATABASE_URL --app $APPNAME`
export LOGDNA_KEY=`heroku config:get LOGDNA_KEY --app $APPNAME`
export REDIS_URL=`heroku config:get REDIS_URL --app $APPNAME`
export SENDGRID_API_KEY=`heroku config:get SENDGRID_API_KEY --app $APPNAME`
# kafka part
#export KAFKA_CLIENT_CERT=`heroku config:get KAFKA_CLIENT_CERT  --app $APPNAME`
#export KAFKA_CLIENT_CERT_KEY=`heroku config:get KAFKA_CLIENT_CERT_KEY  --app $APPNAME`
#export KAFKA_PREFIX=`heroku config:get KAFKA_PREFIX  --app $APPNAME`
#export KAFKA_TRUSTED_CERT=`heroku config:get KAFKA_TRUSTED_CERT  --app $APPNAME`
#export KAFKA_URL=`heroku config:get KAFKA_URL  --app $APPNAME`
#export KAFKA_TOPIC_READ="topicRead"
#export KAFKA_TOPIC_WRITE="topicWrite"
# logs
export LOG_LEVEL=debug
# blower$
