#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
# set me
if [ $# -ne 1 ]
then
    echo "Usage : deploy.sh APPLICATION_NAME"
    exit 1
fi

APPLICATION_NAME=$1

echo "######### Creating the app"
heroku apps:create $APPLICATION_NAME --region eu 

echo "######### Adding Coralogix"
heroku addons:create coralogix:dev --app $APPLICATION_NAME

echo "######### Adding Heroku Postgres addon"git
heroku addons:create heroku-postgresql --app $APPLICATION_NAME

echo "######### Creates databases " 
heroku pg:psql -f createTables.sql --app $APPLICATION_NAME

echo "######### Adding Heroku Connect addon"
HEROKU_API_KEY=`heroku auth:token`
export HEROKU_API_KEY
heroku addons:create herokuconnect --app $APPLICATION_NAME

echo "######### Configuring Heroku Connect Addon"
echo "Enter org name:"
read -s orgname
echo $orgname
echo "Enter Org Password:"
read -s password
echo $password

sfdx shane:heroku:connect -a $APPLICATION_NAME -e production -f jraulouvre.json -u $orgname -p $password > /dev/null

echo "######### Adding Redis addon"
heroku addons:create heroku-redis:premium-0 --app $APPLICATION_NAME

echo "######### Adding Loaderio"
heroku addons:create loaderio:basic --app $APPLICATION_NAME

echo "######### Adding sendgrid"
heroku addons:create sendgrid:starter --app $APPLICATION_NAME
heroku config:set SENDGRID_API_KEY=`FILLME` --app $APPLICATION_NAME
#heroku config:set SENDGRID_API_KEY=`heroku config:get SENDGRID_API_KEY --app jraulouvre` --app $APPLICATION_NAME
#heroku config:set SENDGRID_PASSWORD=`heroku config:get SENDGRID_PASSWORD --app jraulouvre` --app $APPLICATION_NAME
#heroku config:set SENDGRID_USERNAME=`heroku config:get SENDGRID_USERNAME --app jraulouvre` --app $APPLICATION_NAME

echo "######### Adding New relic"
heroku addons:create newrelic:hawke --app $APPLICATION_NAME
NEW_RELIC_LICENSE_KEY=`heroku config:get NEW_RELIC_LICENSE_KEY --app $APPLICATION_NAME`
newrelic-admin generate-config $NEW_RELIC_LICENSE_KEY newrelic.ini
heroku config:add NEW_RELIC_CONFIG_FILE='/app/newrelic.ini'  --app $APPLICATION_NAME
heroku config:add NEW_RELIC_LOG_LEVEL=debug --app $APPLICATION_NAME
heroku config:set NEW_RELIC_APP_NAME="$APPLICATION_NAME" --app $APPLICATION_NAME

echo "######### adding other environment variables"

heroku config:set LOG_LEVEL='DEBUG' --app $APPLICATION_NAME
heroku config:set APPNAME=$APPLICATION_NAME --app $APPLICATION_NAME


echo "######### Pushing sources"

git push heroku master


