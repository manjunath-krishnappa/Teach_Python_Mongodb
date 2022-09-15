import os
import threading
from threading import Thread
import time
import pymongo
from TestBase import MONGO_URL, MONGO_DB_NAME, COLL_NAME1
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from Logger import logger as log
from Utils import random_number, get_current_time_in_epoch


def get_doc_from_mongo1(count):
    listOfResponseTimes = list()
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        for _ in range(1, count):
            before = get_current_time_in_epoch()
            find_one_result = content_file.find_one({'size': _})
            log.info(find_one_result['name'] + " \t " + str(find_one_result['size']))
            after = get_current_time_in_epoch()
            time_diff = after - before
            listOfResponseTimes.append(time_diff)
    except ConfigurationError:
        print("ConfigurationError")
    except ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
    finally:
        return listOfResponseTimes


def get_doc_from_mongo():
    print("get_doc_from_mongo assigned to thread    : {}".format(threading.current_thread().name))
    #print("ID of process running get_doc_from_mongo : {}".format(os.getpid()))
    time_diff = None
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        before = (time.time()) / 1000

        random_num = random_number(1, 100)
        random_num = 123456789
        find_one_result = content_file.find_one({'size': random_num})
        if find_one_result is not None:
            log.info(find_one_result['name'] + " \t " + str(find_one_result['size']))
        else:
            log.info("Query returned None")
        after = (time.time()) / 1000
        time_diff = after - before
    except ConfigurationError:
        print("ConfigurationError")
    except ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
    finally:
        log.info("thread {} : epoch ms before get query   : {}".format(threading.current_thread().name, before))
        log.info("thread {} : epoch ms after  get query   : {}".format(threading.current_thread().name, after))
        log.info("thread {} : time_diff                   : {}".format(threading.current_thread().name, time_diff))
    return time_diff


def TriggerThreads():
    t1 = Thread(target=get_doc_from_mongo, args=(), name='t1')
    t2 = Thread(target=get_doc_from_mongo, args=(), name='t2')
    t3 = Thread(target=get_doc_from_mongo, args=(), name='t3')
    t4 = Thread(target=get_doc_from_mongo, args=(), name='t4')
    t5 = Thread(target=get_doc_from_mongo, args=(), name='t5')
    t6 = Thread(target=get_doc_from_mongo, args=(), name='t6')
    t7 = Thread(target=get_doc_from_mongo, args=(), name='t7')
    t8 = Thread(target=get_doc_from_mongo, args=(), name='t8')
    t9 = Thread(target=get_doc_from_mongo, args=(), name='t9')
    t10 = Thread(target=get_doc_from_mongo, args=(), name='t10')

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()


if __name__ == '__main__':
    for _ in range(1, 11):
        log.info("")
        log.info("Loop : " + str(_))
        TriggerThreads()

    # listOfResponseTimes = get_doc_from_mongo(100)
    #
    # sum_of_response_time = 0;
    # for response_time in listOfResponseTimes:
    #     log.info("response_time get : " + str(response_time) + " \t ms")
    #     sum_of_response_time += response_time
    #
    # avg_response_time = sum_of_response_time / len(listOfResponseTimes)
    #
    # log.info("\n average response_time get : " + str(avg_response_time) + " \t ms")
