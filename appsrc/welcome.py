from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache
from appsrc import app, logger
import traceback

#GUESTFILE = "guest_v2.html"
WELCOME = "jraulouvre/welcome.html"

@app.route('/', methods=['GET'])
def guest():
    try:
        cookie, cookie_exists =  utils.getCookie()

        logger.debug(utils.get_debug_all(request))
        Maxrange = 2
        #time for SQL request
        beginSQL = datetime.now()
        for i in range(0,Maxrange):
            result = postgres.getShifts()
        endSQL = datetime.now()
        logger.info("PG Time : {}'".format(endSQL - beginSQL))
        #logger.info(result)
     
        key={'shifts' : 'available'}
        content = ujson.dumps(result)
        rediscache.__setCache(key, content, 3600)

        beginRedis = datetime.now()
        for i in range(0,Maxrange):
            result = ujson.loads(rediscache.__getCache(key))
        endRedis = datetime.now()
        logger.info("Redis Time : {}'".format(endRedis - beginRedis))
        #logger.info(result)



        #data = render_template(GUESTFILE, form=form, hosts=hosts['data'],userid=cookie,PUSHER_KEY=notification.PUSHER_KEY)

        return utils.returnResponse("hello", 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse("An error occured, check logDNA for more information", 200, cookie, cookie_exists)

        