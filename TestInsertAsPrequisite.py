import time
import pymongo
import threading
from Utils import *
from TestBase import *
from Logger import logger as log
from threading import Thread
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError


def get_random_content_file(num):
    result = dict()
    result["name"] = "cf-" + num
    result["groupId"] = get_uuid()
    result["fileVersion"] = "v" + str(random_number(1, 9))
    result["type"] = "LOGO"
    result["checksum"] = random_string_lowercase()
    result["size"] = num
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


def insert_doc_into_mongo(num):
    print("insert_doc_into_mongo assigned to thread    : {}".format(threading.current_thread().name))

    time_diff = None
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        before = (time.time()) / 1000

        data = get_random_content_file(num)
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

if __name__ == '__main__':

    for _ in range(1, 10001):
        log.info("")
        log.info("Loop : " + str(_))
        insert_doc_into_mongo(_)
