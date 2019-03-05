from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache
from appsrc import app, logger, variables
import traceback


@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def welcome():
    try:
        cookie, cookie_exists =  utils.getCookie()
        datebegin = datetime.now()
        
        language='fr'
        redisKey = variables.KEY_REDIS_WELCOME 
        template = variables.WELCOME
        if ('language' in request.args):
            if (request.args['language'] != None and request.args['language'] != ''):
                if request.args['language'] == 'en':
                    language = 'en'
                    redisKey = variables.KEY_REDIS_WELCOME_EN
                    template = variables.WELCOME_EN

        tmp_content = rediscache.__getCache(redisKey)
        if (tmp_content != '' and tmp_content != None):
            data = tmp_content.decode('UTF-8')
            logger.info('returning redis')
        else:
            logger.info('rendering')
            data = render_template(template, language=language)
            rediscache.__setCache(redisKey, data.encode(), 10)
        

        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))
        #data = render_template(WELCOME)

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE,
        ErrorMessageEn="An error occured, please try again later.",
        ErrorMessageFr="Une erreur est survenue, merci de renouveller votre requête plus tard."), 404, cookie, cookie_exists)

        