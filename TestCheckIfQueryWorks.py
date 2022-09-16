import threading

import pymongo
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from Logger import logger as log
from TestBase import MONGO_URL, MONGO_DB_NAME, COLL_NAME1
from Utils import random_number

if __name__ == '__main__':

    for _ in range(1, 10):
        client = None

        try:
            if client is None:
                client = pymongo.MongoClient(MONGO_URL)

            client.get_database(MONGO_DB_NAME)
            db = client.content_db
            content_file = db.get_collection(COLL_NAME1)
            user = 'admin-tenant-' + str(random_number(1, 1000))
            find_one_result = content_file.find_one({'createdBy': user})

            if find_one_result is not None:
                log.info(find_one_result['name'] + " \t " + str(find_one_result['size']))
            else:
                log.info(" Query returned None for thread {} : and createdBy user : {}".
                         format(threading.current_thread().name, user)
                         )
        except ConfigurationError:
            log.error("ConfigurationError")
        except ServerSelectionTimeoutError:
            log.error("ServerSelectionTimeoutError")