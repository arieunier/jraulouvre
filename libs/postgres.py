from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime 
import os , ujson
import uuid
from libs import utils , logs , rediscache
import random 

DATABASE_URL = os.getenv('DATABASE_URL','')
USE_DB = os.getenv('US_DB','True')
MANUAL_ENGINE_POSTGRES = None
SALESFORCE_SCHEMA = os.getenv("POSTGRES_SCHEMA", "salesforce")
HEROKU_LOGS_TABLE = os.getenv("HEROKU_LOGS_TABLE", "heroku_logs__c") 

logger = logs.logger_init(loggername='app',
            filename="log.log",
            debugvalue=logs.LOG_LEVEL,
            flaskapp=None)

if (DATABASE_URL != '' and USE_DB == 'True'):
    Base = declarative_base()
    MANUAL_ENGINE_POSTGRES = create_engine(DATABASE_URL, pool_size=30, max_overflow=0)
    Base.metadata.bind = MANUAL_ENGINE_POSTGRES
    dbSession_postgres = sessionmaker(bind=MANUAL_ENGINE_POSTGRES)
    session_postgres = dbSession_postgres()
    logger.info("{} - Initialization done Postgresql ".format(datetime.now()))

def __execRequestWithNoResult(strReq, attributes=None):
    if (MANUAL_ENGINE_POSTGRES != None):
        result = MANUAL_ENGINE_POSTGRES.execute(strReq, attributes)


def __execRequest(strReq, Attributes):
    if (MANUAL_ENGINE_POSTGRES != None):
        result = MANUAL_ENGINE_POSTGRES.execute(strReq, Attributes)
        return utils.__resultToDict(result)
    return {'data' : [], "columns": []}

def getShifts():
    sql_request = """
            select Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed 
            from public.Shift 
            where ShiftCurrentConfirmed < ShiftTotalSeats
            order by Id ASC
    """
    data = __execRequest(sql_request, None)
    for entry in data['data']:
        entry['shiftdateiso'] = entry['shiftdate'].strftime("%d-%m-%Y")
    return data

def getVoluntaries():
    sql_request = """
        select Id, Firstname, Lastname, Birthdate, Email, Telephone, ShiftId, RegistrationStatus, ConfirmationCode, Creation_Date 
        from public.voluntary order by Creation_Date DESC
        """
    result = __execRequest(sql_request, None)
    return result


def isUserAlreadyRegistered(email):
    sql_Request = """
        select Id, RegistrationStatus from public.voluntary where LOWER(Email)=LOWER(%(Email)s) 
    """
    result = __execRequest(sql_Request, {'Email' : email} )
    logger.info(result)
    if (len(result['data']) > 0):
        for entry in result['data']:
            logger.info(entry)
            if entry['registrationstatus'] == 'CONFIRMED':
                logger.info("user is already registered, must reject it")
                return True
    return False

def incShiftConfirmed(ShiftId):
    sqlUpdate = "update public.Shift set ShiftCurrentConfirmed = ShiftCurrentConfirmed + 1 where Id = %(ShiftId)s"
    params = {"ShiftId": ShiftId,}
    __execRequestWithNoResult(sqlUpdate, params)    

def insertVoluntary(Firstname, Lastname, Birthdate, Email, Telephone, ShiftId, Cookie, ConfirmationCode, Id):
    sql_request = """
        insert into public.voluntary(Id, Firstname, Lastname, Birthdate,
        Email, Telephone, ShiftId, RegistrationStatus, ConfirmationCode, CookieId, creation_date )
        values
        (%(Id)s, %(Firstname)s, %(Lastname)s, %(Birthdate)s, %(Email)s,
        %(Telephone)s, %(ShiftId)s, %(RegistrationStatus)s, %(ConfirmationCode)s,
        %(CookieId)s, now())
    """
    params = {"Id": Id,
    "Firstname": Firstname,
    "Lastname" : Lastname,
    "Birthdate" : Birthdate,
    "Telephone": Telephone,
    "Email" : Email,
    "ShiftId": ShiftId,
    "RegistrationStatus" : "CONFIRMED",
    "ConfirmationCode" : ConfirmationCode,
    "CookieId":  Cookie}
    logger.info(params)
    __execRequestWithNoResult(sql_request, params)

    incShiftConfirmed(ShiftId)

def getShiftById(Id):
    return __execRequest('Select Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime from public.Shift where Id=%(Id)s', {'Id':Id})

def getUserById(Id):
    return __execRequest('Select Id, ShiftId, RegistrationStatus, ConfirmationCode from public.voluntary where Id=%(Id)s', {'Id':Id})

def unregisterVoluntary(Id, ConfirmationCode, ShiftId):
    # checks user exist
    sql = """
        update public.voluntary set RegistrationStatus = 'CANCELLED' where
        Id=%(Id)s and ConfirmationCode=%(ConfirmationCode)s
        """
    __execRequestWithNoResult(sql, {'Id':Id, 'ConfirmationCode':ConfirmationCode})

    sql = """
        update public.shift set ShiftCurrentConfirmed = ShiftCurrentConfirmed - 1 where
        Id=%(ShiftId)s
        """
    __execRequestWithNoResult(sql, {'ShiftId':ShiftId})
