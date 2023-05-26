# jscom-microblog

A microblog backend for [my personal website](https://www.johnsosoka.com/bits/) . Built with python, flask, peewee, 
sqlite3 & chatGPT.

This is a very simple microblog service. It allows a single user, the admin to publish, edit & delete tiny posts. For 
clients, it allows for the fetching of all posts or a single post. 

Example client get all posts

```json
[
    {
        "content": " Post with a link to <a href=\"https://www.johnsosoka.com\">my website</a>. If it works as expected, it should be saved to the db as an href.",
        "created": "Tue, 23 May 2023 19:01:42 GMT",
        "edited": "Wed, 24 May 2023 17:28:26 GMT",
        "id": 1
    },
    {
        "content": "Another microblog post, look at me go..",
        "created": "Tue, 23 May 2023 19:02:00 GMT",
        "edited": "Tue, 23 May 2023 19:02:00 GMT",
        "id": 2
    }
]
```

## Getting Started

1. Install requirements, `pip install -r requirements.txt`
2. Initialize the database.
   1. navigate to initialization script `cd ./etc/` 
   2. execute initialization script `python3 initialize_db.py`
   3. if prompted, create a username & password. Save these, they will be required for basic http auth on authenticated admin requests.

The above should have created a new file `microblog.db` in the root folder of the project directory. You should now be
able to run the application, `python3 ./app.py`

### Postman

Optionally, you can import the postman collection located in the `./etc/postman` directory.

## API Methods

### Admin

All admin routes require basic http auth. If a user does not exist, you should have been prompted to create a new user 
when running the `initialize_db.py` script from before.

#### CREATE POST
- **Endpoint:** `/v1/micro-blog/admin/posts`
- **Method:** `POST`
- **Description:** Creates a new post.
- **Payload:**
    ```json
    {
        "post_text": "Ensuring I can still create posts"
    }
    ```
- **Example Response:**
    ```json
    {"status": "success"}
    ```

#### FETCH POSTS (admin)
- **Endpoint:** `/v1/micro-blog/admin/posts`
- **Method:** `GET`
- **Description:** Fetches all posts. The admin fetch also returns posts where `visible=0`.
- **Example Response:**
    ```json
    [
    {
        "content": " Post with a link to <a href=\"https://www.johnsosoka.com\">my website</a>. If it works as expected, it should be saved to the db as an href.",
        "created": "Tue, 23 May 2023 19:01:42 GMT",
        "edited": "Wed, 24 May 2023 17:28:26 GMT",
        "id": 1,
        "visible": 1
    },
    {
        "content": "Another microblog post. My ears have been popping.",
        "created": "Tue, 23 May 2023 19:02:00 GMT",
        "edited": "Tue, 23 May 2023 19:02:00 GMT",
        "id": 2,
        "visible": 1
    },
    {
        "content": "Just creating tons of content..",
        "created": "Tue, 23 May 2023 19:02:15 GMT",
        "edited": "Tue, 23 May 2023 19:02:15 GMT",
        "id": 3,
        "visible": 1
    },
    {
        "content": "checking response codes on post create. Should be getting a 201",
        "created": "Tue, 23 May 2023 20:51:13 GMT",
        "edited": "Wed, 24 May 2023 17:30:10 GMT",
        "id": 4,
        "visible": 0
    }
    ]
    ```

#### FETCH POST (admin)
- **Endpoint:** `/v1/micro-blog/admin/posts/{id}`
- **Method:** `GET`
- **Description:** Fetches a specific post for a given post id The admin fetch also returns posts where `visible=0`.
- **Example Response:**
    ```json
    {
    "content": "checking response codes on post create. Should be getting a 201",
    "created": "Tue, 23 May 2023 20:51:13 GMT",
    "edited": "Wed, 24 May 2023 17:30:10 GMT",
    "id": 4,
    "visible": 0
    }
    ```

#### UPDATE POST (admin)
- **Endpoint:** `/v1/micro-blog/admin/posts/{id}`
- **Method:** `PUT`
- **Description:** Updates an existing post. Only respects changing the content & visible fields, service ignores all others.
- **Payload:**
    ```json
    {
        "content": " Post with a link to <a href=\"https://www.johnsosoka.com\">my website</a>. If it works as expected, it should be saved to the db as an href. Making another change",
        "id": 1,
        "visible": 1
    }
    ```
- **Example Response:**

    **204 NO CONTENT**

#### HEALTHCHECK
- **Endpoint:** `/healthcheck`
- **Method:** `GET`
- **Example Response:**
    ```
    Good.
    ```
  
### Client

#### FETCH POSTS (client)
- **Endpoint:** `/v1/micro-blog/posts`
- **Method:** `GET`
- **Example Response:**
    ```json
    [
    {
    "content": "Just creating tons of content..",
    "created": "Tue, 23 May 2023 19:02:15 GMT",
    "edited": "Tue, 23 May 2023 19:02:15 GMT",
    "id": 3
    },
    {
    "content": "checking response codes on post create. Should be getting a 201",
    "created": "Tue, 23 May 2023 21:00:37 GMT",
    "edited": "Tue, 23 May 2023 21:00:37 GMT",
    "id": 5
    },
    {
    "content": "Using chatGPT as a copilot has been legit!",
    "created": "Tue, 23 May 2023 21:17:43 GMT",
    "edited": "Tue, 23 May 2023 21:17:43 GMT",
    "id": 6
    },
    {
    "content": "Ensuring I can still create posts",
    "created": "Wed, 24 May 2023 06:44:00 GMT",
    "edited": "Wed, 24 May 2023 06:44:00 GMT",
    "id": 7
    },
    {
    "content": "Test post creation",
    "created": "Wed, 24 May 2023 17:53:17 GMT",
    "edited": "Wed, 24 May 2023 17:53:17 GMT",
    "id": 8
    }
    ]
    ```

#### FETCH POST (client)
- **Endpoint:** `/v1/micro-blog/posts/7`
- **Method:** `GET`
- **Example Response:**
    ```json
    [
    {
        "content": "Ensuring I can still create posts",
        "created": "Wed, 24 May 2023 06:44:00 GMT",
        "edited": "Wed, 24 May 2023 06:44:00 GMT",
        "id": 7
    }
    ]
    ```


## TODO
- [ ] JWT Auth
- [x] Implement pagination
- [ ] YML config / support multiple env configs
- [ ] Dockerize
- [ ] Blueprint service based healthcheck.
- [x] Secure admin endpoints
- [x] Tidy up / parameterize Postman with env configs

