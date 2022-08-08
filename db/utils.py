from db.connect import DB
from db.config import DB_NAME

db = DB(DB_NAME)


def init_user(user_id, username):
    return db.add_user_to_db(user_id, username)
