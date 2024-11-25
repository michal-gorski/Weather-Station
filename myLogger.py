import datetime
import logging

def Log(text:str):
    logger = logging.getLogger(__name__)
    logger.info(text)
    print(datetime.datetime.now(),': ',text)