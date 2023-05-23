# jscom-microblog
A microblog backend for www.johnsosoka.com



# TODO
- logging
- service & controller for clients

# Plan

* jsonschema for request validation
* Flask - web, MVC
* Peewee
* Sqlite3 for db


**POST**
- ID (int)
- content (str)
- created (timestamp)
- visible (boolean)
- deleted (timestamp)
- edited (timestamp)

Note: Should we save previous versions of posts to a different table? Something like an audit log