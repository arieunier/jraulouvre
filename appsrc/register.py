from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache, sendmail
from appsrc import app, logger, variables
import traceback
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateField
import random



class ReusableForm(Form):
    Firstname = TextField('Firstname', validators=[validators.required()])
    Lastname = TextField('Lastname', validators=[validators.required()])
    Birthdate = DateField('Birthdate', validators=[validators.required()])
    Telephone = TextField('Telephone', validators=[validators.required()])
    Email = TextField('Email', validators=[validators.required()])
    EmailConfirmation = TextField('EmailConfirmation', validators=[validators.required()])
    ShiftId = TextField('ShiftId', validators=[validators.required()])
    
@app.route('/register.html', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        cookie, cookie_exists =  utils.getCookie()
        logger.debug(utils.get_debug_all(request))
        datebegin = datetime.now()
        
        
        form = ReusableForm(request.form)
        if (request.method == 'POST' and variables.ACCEPT_REGISTRATION == 'True'):
            Firstname=request.form['Firstname']
            Lastname=request.form['Lastname']
            Telephone=request.form['Telephone']
            Email=request.form['Email'].strip()
            Birthdate=request.form['Birthdate']
            EmailConfirmation=request.form['EmailConfirmation'].strip()
            ShiftId=request.form['Shift']
            
            
            #now we call the DB everytime to make sure we have place
            shiftAvail = postgres.getShifts()
            isShiftAvailable = False
            # is the shift still available ?
            for shift in shiftAvail['data']:
                if (shift['id'] == ShiftId):
                    isShiftAvailable = True
                    logger.info("Shift Id {} still Available - {}/{}".format(ShiftId, 
                        shift['shiftcurrentconfirmed'], shift['shifttotalseats']))
                    break

            if (isShiftAvailable == False):
                # need to display an error and reload
                logger.info("Shift Id {} Not Available ".format(ShiftId))
                data = render_template(variables.REGISTER, form=form, shifts=shiftAvail['data'], 
                    ErrorMessageEn="This shift is now full, please select another one.",
                    ErrorMessageFr="Cette session est désormais pleine, merci d'en choisir une autre.")
            else:
                # is user already registered with another shift 
                if (postgres.isUserAlreadyRegistered(Email) == True):
                    data = render_template(variables.REGISTER, form=form, shifts=shiftAvail['data'], 
                        ErrorMessageEn="You are already registered to a shift. Please cancel your registration first by clicking the link send by email.",
                        ErrorMessageFr="Vous êtes déjà enregistré à une session. Veuillez d'abord annuler celle ci en cliquant sur le lien reçu par email.")
                    
                else:
                    # ok now we an add the user
                    ConfirmationCode=  random.randint(0, 10000)
                    Id = uuid.uuid4().__str__()
                    postgres.insertVoluntary(Firstname, Lastname, Birthdate, Email, Telephone, ShiftId, cookie, ConfirmationCode, Id)
                    # flush redis
                    rediscache.__delCache(variables.KEY_REDIS_SHIFTS)
                    # sends an email
                    # gets the shift name
                    shift = postgres.getShiftById(ShiftId)

                    sendmail.sendEmail(Email, Firstname, Lastname, Birthdate, ConfirmationCode, Id, shift['data'][0]['shiftnamefr'], Telephone)
                    data = render_template(variables.THANKS)
                
        else:
                    
            # checks if we have in Redis the current shifts availability
            shiftsAvailBinary = rediscache.__getCache(variables.KEY_REDIS_SHIFTS)
            shiftAvail = {}
            if (shiftsAvailBinary == '' or shiftsAvailBinary == None):
                # gets the current Shift and saves them in redis for others
                shiftAvail = postgres.getShifts()
                rediscache.__setCache(variables.KEY_REDIS_SHIFTS, ujson.dumps(shiftAvail), 60)
            else:
                shiftAvail = ujson.loads(shiftsAvailBinary)

            # check now the len of the available shifts
            logger.info("Remaining Shifts: {}".format(len(shiftAvail['data'])))
            if (len(shiftAvail['data']) == 0):
                return utils.returnResponse(render_template(variables.ERROR_PAGE, 
                ErrorMessageEn="Registrations are closed: there is no more shift available. ",
                ErrorMessageFr="Les inscriptions sont suspendues: il n'y a plus de place disponible."), 200, cookie, cookie_exists)
            else:
                #logger.info("has shift")
                #logger.info(shiftAvail['data'])
                data = render_template(variables.REGISTER, form=form, shifts=shiftAvail['data'])

        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE, 
        ErrorMessageEn="An error occured, please try again later.",
        ErrorMessageFr="Une erreur est survenue, merci de renouveller votre requête plus tard."), 404, cookie, cookie_exists)

        