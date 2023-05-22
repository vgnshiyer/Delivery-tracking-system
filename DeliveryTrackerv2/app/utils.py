from pymongo import MongoClient
def get_db_handle(db_name, host, port):

    client = MongoClient(host=host,
                        port=int(port)
                        )
    db_handle = client[db_name]
    return db_handle, client