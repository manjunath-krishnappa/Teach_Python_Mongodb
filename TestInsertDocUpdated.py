import time
import pymongo
import threading
from Utils import *
from TestBase import *
from Logger import logger as log
from threading import Thread
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError


def get_random_content_file():
    result = dict()
    result["name"] = "cf-" + uuid.uuid4().hex
    result["groupId"] = get_uuid()
    result["fileVersion"] = "v" + str(random_number(1, 9))
    result["type"] = "LOGO"
    result["checksum"] = random_string_lowercase()
    result["size"] = random_number(1, 10000)
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
        log.info("thread {} : epoch ms before get query   : {}".format(threading.current_thread().name, before))
        log.info("thread {} : epoch ms after  get query   : {}".format(threading.current_thread().name, after))
        log.info("thread {} : time_diff                   : {}".format(threading.current_thread().name, time_diff))
    except ConfigurationError:
        print("ConfigurationError")
    except ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")

    return time_diff


def TriggerThreads(nThreadsPerSec):
    listOfThreads = list()

    for num in range(1, nThreadsPerSec + 1):
        listOfThreads.append(Thread(target=insert_doc_into_mongo, args=(), name='t' + str(num)))

    for thread in listOfThreads:
        thread.start()

    for thread in listOfThreads:
        thread.join()


if __name__ == '__main__':

    nThreadsPerSec = 10

    for _ in range(1, 11):
        log.info("")
        log.info("Loop : " + str(_))
        TriggerThreads(nThreadsPerSec)
