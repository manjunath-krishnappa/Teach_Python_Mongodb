import time
import pymongo
from TestBase import MONGO_URL, MONGO_DB_NAME, COLL_NAME1
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from Logger import logger as log


def get_doc_from_mongo(count):
    listOfResponseTimes = list()
    try:
        client = pymongo.MongoClient(MONGO_URL)
        client.get_database(MONGO_DB_NAME)
        db = client.content_db
        content_file = db.get_collection(COLL_NAME1)
        for _ in range(1, count):
            before = (time.time()) / 1000
            find_one_result = content_file.find_one({'size': _})
            log.info(find_one_result['name'] + " \t " + str(find_one_result['size']))
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
    listOfResponseTimes = get_doc_from_mongo(100)

    sum_of_response_time = 0;
    for response_time in listOfResponseTimes:
        log.info("response_time get : " + str(response_time) + " \t ms")
        sum_of_response_time += response_time

    avg_response_time = sum_of_response_time / len(listOfResponseTimes)

    log.info("\n average response_time get : " + str(avg_response_time) + " \t ms")
