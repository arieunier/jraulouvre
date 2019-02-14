from flask import Flask, request, redirect, url_for, render_template
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache


TEMPLATES_URL = "../templates"
STATIC_URL = "../static"
# environment variable
WEBPORT = os.getenv('PORT', '5000')



app = Flask(__name__, template_folder=TEMPLATES_URL, static_folder=STATIC_URL) 
#Flask(app)

logs.logger_init(loggername='app',
            filename="log.log",
            debugvalue=logs.LOG_LEVEL,
            flaskapp=app)

logger = logs.logger 


