import threading
import time
from threading import Thread

import pymongo
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from Logger import logger as log
from TestBase import *
from Utils import *


def get_random_content_file():
    result = dict()
    result["name"] = "cf-" + uuid.uuid4().hex
    result["groupId"] = get_uuid()
    result["fileVersion"] = "v" + str(random_number(1, 9))
    result["type"] = "LOGO"
    result["checksum"] = random_string_lowercase()
    result["size"] = random_number(100, 10000)
    result["url"] = "http://url.com"
    result["description"] = "DESC"
    result["uploadedBy"] = "SERVICEPROVIDER_ADMIN"
    result["uploadAdminEmail"] = "admin@admin.com"
    result["windowsVersion"] = "Windows-" + random_string_lowercase()
    result["osBuildVersion"] = "osBuildVersion-" + random_string_lowercase()
    result["deleted"] = False
    result["enabled"] = True
    result["repoType"] = random_number(1, 9999)
    result["imageType"] = random_number(1, 9999)
    result["parentTenantIdFolder"] = "f-tenant-folder-" + random_string_lowercase()
    result["tenantIdFolder"] = "t-folder-" + random_string_lowercase()
    result["parentTenant"] = get_uuid()
    result["serviceId"] = "CMS"
    result["tenant"] = get_uuid()
    result["createdBy"] = "admin"
    result["createdOn"] = random_number(1, 9999)
    return result


def insert_doc_into_mongo():
    print("insert_doc_into_mongo assigned to thread    : {}".format(threading.current_thread().name))

    time_diff = None
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        before = (time.time()) / 1000

        data = get_random_content_file()
        insert_result = content_file.insert_one(data)
        if insert_result is not None and insert_result.acknowledged:
            log.info(data['name'] + " inserted \t successfully")
        else:
            log.info(data['name'] + " inserted \t failed")

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
    t1 = Thread(target=insert_doc_into_mongo, args=(), name='t1')
    t2 = Thread(target=insert_doc_into_mongo, args=(), name='t2')
    t3 = Thread(target=insert_doc_into_mongo, args=(), name='t3')
    t4 = Thread(target=insert_doc_into_mongo, args=(), name='t4')
    t5 = Thread(target=insert_doc_into_mongo, args=(), name='t5')
    t6 = Thread(target=insert_doc_into_mongo, args=(), name='t6')
    t7 = Thread(target=insert_doc_into_mongo, args=(), name='t7')
    t8 = Thread(target=insert_doc_into_mongo, args=(), name='t8')
    t9 = Thread(target=insert_doc_into_mongo, args=(), name='t9')
    t10 = Thread(target=insert_doc_into_mongo, args=(), name='t10')

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
