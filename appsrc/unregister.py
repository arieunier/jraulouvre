from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache
from appsrc import app, logger, variables
import traceback
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateField



class ReusableForm(Form):
    ConfirmationCode = TextField('ConfirmationCode', validators=[validators.required()])


@app.route('/unregister', methods=['GET', 'POST'])
def unregister():
    try:
        cookie, cookie_exists =  utils.getCookie()
        logger.debug(utils.get_debug_all(request))
        datebegin = datetime.now()
        
        language=utils.getBrowserLanguage(request)
        if ('language' in request.args):
            if (request.args['language'] != None and request.args['language'] != ''):
                if request.args['language'] == 'en':
                    language = 'en'
                elif request.args['language'] == 'fr':
                    language = 'fr'
                    
        logger.info(language)
        form = ReusableForm(request.form)
        if request.method == 'POST':
            ConfirmationCode=request.form['ConfirmationCode']
            Id=request.form['Id']
            userContent = postgres.getUserById(Id) 
            logger.info(userContent)
            # if user is incorrect, or if already cancelled, or if confirmation code does not match:
            if (
                (len(userContent['data']) == 0) or 
                (userContent['data'][0]['registrationstatus'] != 'CONFIRMED') or
                (userContent['data'][0]['confirmationcode'] != ConfirmationCode)  ) :
                logger.error("Incorrect configuration for {}/{} => {}/{}".format(Id, 
                    ConfirmationCode, 
                    userContent['data'][0]['registrationstatus'], 
                    userContent['data'][0]['confirmationcode'] ))
                
                doc = variables.UNREGISTER[language]


                return utils.returnResponse(render_template(doc , 
                form=form, Id=Id, 
                ErrorMessage=variables.CODE_MISMATCH[language], language=language), 200, cookie, cookie_exists)
        
            
            # status is correct, lets check if 
            postgres.unregisterVoluntary(Id, ConfirmationCode, userContent['data'][0]['shiftid'])
            rediscache.__delCache(variables.KEY_REDIS_SHIFTS)
            doc = variables.UNREGISTER_SUCCESS[language]
            data = render_template(doc)

        else:
            # gets the id
            if ('Id' not in request.args):
                logger.error("Missing Id in Request")
                return utils.returnResponse(render_template(variables.ERROR_PAGE, 
                ErrorMessage=variables.CODE_MISMATCH[language], language=language), 200, cookie, cookie_exists)
            Id = request.args['Id']                

            #logger.info("Id={}".format(Id))
            
            userContent = postgres.getUserById(Id) 
            #logger.info(userContent)
            if (len(userContent['data']) == 0):
                logger.error("Unknown user {}".format(Id))
                return utils.returnResponse(render_template(variables.ERROR_PAGE, 
                ErrorMessage=variables.CODE_MISMATCH[language], language=language), 200, cookie, cookie_exists)

            # render the page
            doc = variables.UNREGISTER[language]
            data = render_template(doc, form=form, Id=Id)

        
        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE, 
        ErrorMessage=variables.ERROR_GENERIC[language], language=language), 200, cookie, cookie_exists)

        