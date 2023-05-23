from entity.post import Post
from dao.database import db

def initialize_database():
     db.create_tables([Post])

print("initializing database...")
initialize_database()
print("done.")