from entity.post import Post
from dao.database import db


def initialize_database():
    db.create_tables([Post])


print("initializing database...")
try:
    initialize_database()
except Exception as e:
    print("Something went wrong...")
    print(str(e))

print("finished.")
