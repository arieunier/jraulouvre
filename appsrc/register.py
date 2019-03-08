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
    #Telephone = TextField('Telephone', validators=[validators.required()])
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
        
        Preferred_Language=utils.getBrowserLanguage(request)

        thanks = variables.THANKS
        if ('language' in request.args):
            if (request.args['language'] != None and request.args['language'] != ''):
                if request.args['language'] == 'en':
                    Preferred_Language = 'en'
                elif request.args['language'] == 'fr':
                    Preferred_Language = 'fr'                    
                    
        template = variables.REGISTER[Preferred_Language]

        form = ReusableForm(request.form)
        if (request.method == 'POST' and variables.ACCEPT_REGISTRATION == 'True'):
            Firstname=request.form['Firstname']
            Lastname=request.form['Lastname']
            #Telephone=request.form['Telephone']
            Telephone="+33612345678"
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
            # test is more than 18yo
            currentDate = datetime.now()
            Pattern ="%Y-%m-%d"
            if ("/" in Birthdate):
                Pattern = "%Y/%m/%d"
            birthdateDate = datetime.strptime(Birthdate, Pattern)
            diffDates = currentDate - birthdateDate
            if (diffDates.days < 6570): #18 * 365:
                data = render_template(template, language=Preferred_Language, form=form, shifts=shiftAvail['data'], 
                        ErrorMessage=variables.AGE_LIMIT[Preferred_Language])
                return utils.returnResponse(data, 200, cookie, cookie_exists)                 
            logger.info(Preferred_Language)
            # test emails match
            if (Email != EmailConfirmation):
                data = render_template(template, language=Preferred_Language, form=form, shifts=shiftAvail['data'], 
                        ErrorMessage=variables.EMAILS_MISMATCH[Preferred_Language])
                return utils.returnResponse(data, 200, cookie, cookie_exists)    


        

            if (isShiftAvailable == False):
                # need to display an error and reload
                logger.info("Shift Id {} Not Available ".format(ShiftId))
                data = render_template(template, language=Preferred_Language, form=form, shifts=shiftAvail['data'], 
                    ErrorMessage=variables.SHIFT_FULL[Preferred_Language])
            else:
                # is user already registered with another shift 
                if (postgres.isUserAlreadyRegistered(Email) == True):
                    data = render_template(template, language=Preferred_Language, form=form, shifts=shiftAvail['data'], 
                        ErrorMessage=variables.ALREADY_REGISTERED[Preferred_Language])
                    
                else:
                    # ok now we an add the user
                    ConfirmationCode=  random.randint(0, 10000)
                    Id = uuid.uuid4().__str__()
                    postgres.insertVoluntary(Firstname, Lastname, Birthdate, Email, Telephone, ShiftId, cookie, ConfirmationCode, Id, Preferred_Language)
                    # flush redis
                    rediscache.__delCache(variables.KEY_REDIS_SHIFTS)
                    # sends an email
                    # gets the shift name
                    shift = postgres.getShiftById(ShiftId)

                    if (Preferred_Language == 'en'):
                        sendmail.sendEmail(Email, Firstname, Lastname, Birthdate, ConfirmationCode, Id, shift['data'][0]['shiftnameen'], Telephone, 'en')
                    else:
                        sendmail.sendEmail(Email, Firstname, Lastname, Birthdate, ConfirmationCode, Id, shift['data'][0]['shiftnamefr'], Telephone, 'fr')
                    data = render_template(thanks, language=Preferred_Language)
                
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
                ErrorMessage=variables.REGISTRATION_CLOSED[Preferred_Language], language=Preferred_Language), 200, cookie, cookie_exists)
            else:
                #logger.info("has shift")
                #logger.info(shiftAvail['data'])
                data = render_template(template, language=Preferred_Language, form=form, shifts=shiftAvail['data'])

        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE, 
        ErrorMessage=variables.ERROR_GENERIC[Preferred_Language], language=Preferred_Language), 404, cookie, cookie_exists)

        