from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os, logging, psycopg2 
from datetime import datetime 
import ujson
import uuid
from libs import postgres , utils , logs, rediscache
from appsrc import app, logger, variables
import traceback
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateField


@app.route('/<filename>', methods=['GET'])
def static_proxy(filename):
    if (filename == None or filename == ''):
        return root()
    return app.send_static_file(filename)

#@app.route('/cestquilpatron', methods=['GET', 'POST'])
def cestquilpatron():
    try:
        cookie, cookie_exists =  utils.getCookie()
        logger.debug(utils.get_debug_all(request))
        datebegin = datetime.now()
        shifts = postgres.getShifts()
        voluntaries = postgres.getVoluntaries()
        data = render_template(variables.ADMIN,
                            columnsShifts=shifts['columns'],
                            entriesShifts = shifts['data'],
                            columnsVoluntaries=voluntaries['columns'],
                            entriesVoluntaries = voluntaries['data'])
        dateend = datetime.now()
        logger.info("time = {}".format(dateend - datebegin))

        return utils.returnResponse(data, 200, cookie, cookie_exists)
    except Exception as e:
        
        traceback.print_exc()
        cookie, cookie_exists =  utils.getCookie()
        return utils.returnResponse(render_template(variables.ERROR_PAGE, error="An error occured, please try again later"), 404, cookie, cookie_exists)

        