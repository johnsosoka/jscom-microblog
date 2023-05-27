import logging
import getpass
from werkzeug.security import generate_password_hash
from entity.post import Post
from entity.user import User
from dao.database import db
from peewee import IntegrityError

logging.basicConfig(level=logging.INFO)

def initialize_database():
    db.create_tables([Post, User])

def create_admin_user():
    username = input("Enter a username for the admin: ")
    password = getpass.getpass("Enter a password for the admin: ")
    hashed_password = generate_password_hash(password)
    try:
        admin = User.create(username=username, password=hashed_password)
        return admin
    except IntegrityError:
        logging.error("A user with this username already exists.")

# This is a 1 user application.
def any_user_exists():
    return User.select().exists()

logging.info("initializing database...")
try:
    initialize_database()
    admin = any_user_exists()
    if admin is None:
        admin = create_admin_user()
        logging.info(f"Admin user created with username: {admin.username}")
    else:
        logging.info(f"Admin user {admin.username} already exists, created at: {admin.created}")
except Exception as e:
    logging.error("Something went wrong...")
    logging.error(str(e))

logging.info("finished.")
