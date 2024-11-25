import datetime
import logging

def Log(text:str):
    logger = logging.getLogger(__name__)
    logger.log(text)
    print(datetime.datetime.now(),': ',text)