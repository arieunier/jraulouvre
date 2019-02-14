from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache
from appsrc import app, logger, variables
import traceback


@app.route('/', methods=['GET'])
def welcome():
    try:
        cookie, cookie_exists =  utils.getCookie()
        datebegin = datetime.now()
        tmp_content = rediscache.__getCache(variables.KEY_REDIS_WELCOME)
        if (tmp_content != '' and tmp_content != None):
            data = tmp_content.decode('UTF-8')
            logger.info('returning redis')
        else:
            logger.info('rendering')
            data = render_template(variables.WELCOME)
            rediscache.__setCache(variables.KEY_REDIS_WELCOME, data.encode(), 10)
        
        """
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
        """

        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))
        #data = render_template(WELCOME)

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE), 200, cookie, cookie_exists)

        