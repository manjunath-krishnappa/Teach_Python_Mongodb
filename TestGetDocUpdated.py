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
        client, db, coll = None, None, None
        time_diff, before, after = None, None, None

        client = pymongo.MongoClient(MONGO_URL)
        db = client.get_database(MONGO_DB_NAME)
        coll = db.get_collection(COLL_NAME1)

        before = (time.time()) / 1000
        user = 'admin-tenant-' + str(random_number(1, 1000))
        find_one_result = coll.find_one({'createdBy': user})

        if find_one_result is not None:
            log.info(find_one_result['name'] + " \t " + str(find_one_result['createdBy']))
        else:
            log.info(" Query returned None for thread {} : and createdBy user : {}".
                     format(threading.current_thread().name, user)
                     )

        after = (time.time()) / 1000
        time_diff_sec = after - before
        time_diff_millisec = time_diff_sec * 1000

        log.info("thread {} : epoch ms before get query   : {}".format(threading.current_thread().name, before))
        log.info("thread {} : epoch ms after  get query   : {}".format(threading.current_thread().name, after))
        log.info("thread {} : time_diff sec               : {}".format(threading.current_thread().name, time_diff_sec))
        log.info("thread {} : time_diff millisec          : {}".format(threading.current_thread().name, time_diff_millisec))
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
