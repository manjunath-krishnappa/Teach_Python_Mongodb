import threading

import pymongo
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from Logger import logger as log
from TestBase import MONGO_URL, MONGO_DB_NAME, COLL_NAME1
from Utils import random_number

if __name__ == '__main__':

    for _ in range(1, 1000):
        client = None

        try:
            if client is None:
                client = pymongo.MongoClient(MONGO_URL)
            #print("MONGO_URL     : " + MONGO_URL)    
            #print("MONGO_DB_NAME : " + MONGO_DB_NAME)
            #print("COLL_NAME1    : " + COLL_NAME1)

            db = client.get_database(MONGO_DB_NAME)
            coll_names = db.list_collection_names()
            print(coll_names)
            content_file = db.get_collection(COLL_NAME1)
            user = 'admin-tenant-' + str(_)
            find_one_result = db.content_file.find_one({'createdBy': user})

            if find_one_result is not None:
                log.info(find_one_result['name'] + " \t " + str(find_one_result['createdBy']))
            else:
                log.info(" Query returned None for thread {} : and createdBy user : {}".
                         format(threading.current_thread().name, user)
                         )
        except ConfigurationError:
            log.error("ConfigurationError")
        except ServerSelectionTimeoutError:
            log.error("ServerSelectionTimeoutError")
