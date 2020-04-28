import redis 
import os
import ujson
from datetime import datetime 
from libs import logs   
import traceback
REDIS_URL = os.getenv('REDIS_URL','')
REDIS_CONN = None 

logger = logs.logger_init(loggername='app',
            filename="log.log",
            debugvalue=logs.LOG_LEVEL,
            flaskapp=None)

def __connect():
    global REDIS_CONN
    global REDIS_URL
    if (REDIS_URL != ''):
        REDIS_CONN = redis.from_url(REDIS_URL)
        REDIS_CONN.set('key','value')
        REDIS_CONN.expire('key', 3600) # 1 hour
        logger.info("{}  - Initialization done Redis" .format(datetime.now()))



def __display_RedisContent():
    try:
        global REDIS_CONN
        if (REDIS_CONN == None):
            __connect()
        if (REDIS_CONN != None):
            for keys in REDIS_CONN.scan_iter():
                logger.info(keys)
        cacheData = __getCache('keys *')
        if cacheData != None:
            for entry in cacheData:
                logger.info(entry)
    except Exception as e:
        REDIS_CONN = None
        traceback.print_exc()

def __setCache(key, data, ttl):
    try:
        global REDIS_CONN
        if (REDIS_CONN == None):
            __connect()

        key_str = ujson.dumps(key)
        logger.info('Key->{}'.format(key_str))
        logger.info('Data->{}'.format(data))

        if (REDIS_CONN != None):
            #logger.debug('Storing in Redis')
            REDIS_CONN.set(key_str, data)
            REDIS_CONN.expire(key_str, ttl)
    except Exception as e:
        REDIS_CONN = None
        traceback.print_exc()

def __getCache(key):
    try:
        global REDIS_CONN
        if (REDIS_CONN == None):
            __connect()

        key_str = ujson.dumps(key)
        if (REDIS_CONN != None):
            #logger.debug('Reading in Redis')
            return REDIS_CONN.get(key_str)
        return None 
    except Exception as e:
        REDIS_CONN = None
        traceback.print_exc()
        return None

def __delCache(key):
    try:
        global REDIS_CONN
        if (REDIS_CONN == None):
            __connect()

        key_str = ujson.dumps(key)
        if (REDIS_CONN != None):
            #logger.debug('Deleting in Redis')
            REDIS_CONN.delete(key_str)
    except Exception as e:
        REDIS_CONN = None
        traceback.print_exc()
    
