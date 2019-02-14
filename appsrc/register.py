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
    Firstname = TextField('Firstname', validators=[validators.required()])
    Lastname = TextField('Lastname', validators=[validators.required()])
    Birthdate = DateField('Birthdate', validators=[validators.required()])
    Telephone = TextField('Telephone', validators=[validators.required()])
    Email = TextField('Email', validators=[validators.required()])
    EmailConfirmation = TextField('EmailConfirmation', validators=[validators.required()])
    ShiftId = TextField('ShiftId', validators=[validators.required()])
    

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
            Email=request.form['Email']
            Birthdate=request.form['Birthdate']
            EmailConfirmation=request.form['EmailConfirmation']
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
            if (isShiftAvailable == 'False'):
                # need to display an error and reload
                data = render_template(variables.REGISTER, form=form, shifts=shiftAvail['data'], error="Yes")


            # is user already registered with another shift 

            
            # ok now we an add the user
            

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
                return utils.returnResponse(render_template(variables.NO_MORE_SHIFT), 200, cookie, cookie_exists)
            else:
                logger.info("has shift")
                logger.info(shiftAvail['data'])
                data = render_template(variables.REGISTER, form=form, shifts=shiftAvail['data'])

        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE), 200, cookie, cookie_exists)

        