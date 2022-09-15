import time

import pymongo

from TestBase import *
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from Utils import *
from Logger import logger as log


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


def insert_into_mongo(count):

    listOfResponseTimes = list()
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        for _ in range(1, count):
            data = get_random_content_file()
            data["size"] = _
            before = (time.time()) / 1000
            insert_result = content_file.insert_one(data)
            log.info(data["name"])
            log.info(insert_result.acknowledged)
            after = (time.time()) / 1000
            time_diff = after - before
            listOfResponseTimes.append(time_diff)
    except ConfigurationError:
        print("ConfigurationError")
    except ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
    finally:
        return listOfResponseTimes


if __name__ == '__main__':

    listOfResponseTimes = insert_into_mongo(10)
    sum_of_response_time = 0;
    for response_time in listOfResponseTimes:
        log.info("response_time insert : " + str(response_time) + " \t ms")
        sum_of_response_time += response_time

    avg_response_time = sum_of_response_time / len(listOfResponseTimes)

    log.info("\n average response_time insert : " + str(avg_response_time) + " \t ms")