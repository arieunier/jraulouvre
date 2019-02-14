from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime 
import os , ujson
import uuid
from libs import utils , logs , rediscache

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
