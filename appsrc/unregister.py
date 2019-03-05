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
        
        language='fr'
        if ('language' in request.args):
            if (request.args['language'] != None and request.args['language'] != ''):
                if request.args['language'] == 'en':
                    language = 'en'

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
                
                if (language =='fr'):
                    doc = variables.UNREGISTER
                else:
                    doc = variables.UNREGISTER_EN

                return utils.returnResponse(render_template(doc , 
                form=form, Id=Id,
                ErrorMessageEn="Incorrect configuration. Can not proceed with unregister action. Please check code given by email.",
                ErrorMessageFr="Configuration incorrrecte, veuillez vérifier le code reçu par email."), 200, cookie, cookie_exists)
        
            
            # status is correct, lets check if 
            postgres.unregisterVoluntary(Id, ConfirmationCode, userContent['data'][0]['shiftid'])
            rediscache.__delCache(variables.KEY_REDIS_SHIFTS)
            if (language =='fr'):
                doc = variables.UNREGISTER_SUCCESS
            else:
                doc = variables.UNREGISTER_SUCCESS_EN

            data = render_template(doc)
        else:
            # gets the id
            if ('Id' not in request.args):
                logger.error("Missing Id in Request")
                return utils.returnResponse(render_template(variables.ERROR_PAGE, error="Incorrect configuration, please provide Id"), 200, cookie, cookie_exists)
            Id = request.args['Id']                

            #logger.info("Id={}".format(Id))
            
            userContent = postgres.getUserById(Id) 
            #logger.info(userContent)
            if (len(userContent['data']) == 0):
                logger.error("Unknown user {}".format(Id))
                return utils.returnResponse(render_template(variables.ERROR_PAGE, error="Incorrect configuration, please check given Id"), 200, cookie, cookie_exists)

            # render the page
            if (language =='fr'):
                doc = variables.UNREGISTER
            else:
                doc = variables.UNREGISTER_EN

            data = render_template(doc, form=form, Id=Id)

        
        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE, 
        ErrorMessageEn="An error occured, please try again later.",
        ErrorMessageFr="Une erreur est survenue, merci de renouveller votre requête plus tard."), 200, cookie, cookie_exists)

        