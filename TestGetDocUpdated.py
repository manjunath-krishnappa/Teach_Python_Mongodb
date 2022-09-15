import os
import threading
from threading import Thread
import time
import pymongo
from TestBase import MONGO_URL, MONGO_DB_NAME, COLL_NAME1
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from Logger import logger as log
from Utils import random_number, get_current_time_in_epoch


def get_doc_from_mongo():

    print("get_doc_from_mongo assigned to thread    : {}".format(threading.current_thread().name))
    try:
        client = None
        time_diff = None
        before = None
        after = None

        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)

        before = (time.time()) / 1000
        random_num = random_number(1, 100)
        find_one_result = content_file.find_one({'size': random_num})

        if find_one_result is not None:
            log.info(find_one_result['name'] + " \t " + str(find_one_result['size']))
        else:
            log.info("Query returned None")

        after = (time.time()) / 1000
        time_diff = after - before

        log.info("thread {} : epoch ms before get query   : {}".format(threading.current_thread().name, before))
        log.info("thread {} : epoch ms after  get query   : {}".format(threading.current_thread().name, after))
        log.info("thread {} : time_diff                   : {}".format(threading.current_thread().name, time_diff)
    except ConfigurationError:
        log.error("ConfigurationError")
    except ServerSelectionTimeoutError:
        log.error("ServerSelectionTimeoutError")

    return time_diff


def TriggerThreads(nThreadsPerSec):

    listOfThreads = list()

    for num in range(1, nThreadsPerSec + 1):
        listOfThreads.append(Thread(target=get_doc_from_mongo, args=(), name='t' + str(num)))

    for thread in listOfThreads:
        thread.start()

    for thread in listOfThreads:
        thread.join()


if __name__ == '__main__':

    nThreadsPerSec = 10

    for _ in range(1, 330):
        log.info("")
        log.info("Loop : " + str(_))
        TriggerThreads(nThreadsPerSec)