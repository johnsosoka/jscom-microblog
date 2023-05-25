from flask import Blueprint, request, Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from entity.user import User
from peewee import DoesNotExist
import datetime

posts_controller_admin = Blueprint('users', __name__)
from service.admin_service import AdminService


admin_service = AdminService()

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        # User not found in the database
        return False

    if check_password_hash(user.password, password):
        # Updates last_login timestamp
        user.last_login = datetime.datetime.now()
        user.save()
        return True

    return False


@posts_controller_admin.route('/posts', methods=['POST'])
@auth.login_required
def create_post():
    response_body = {"status": "success"}
    body = ""
    try:
        body = request.get_json()["post_text"]
    except KeyError as e:
        response_body["status"] = "failure"
        response_body["reason"] = "missing mandatory field, <post_text>"
        return response_body, 400

    # Create the post & return the generated id.
    post_id = admin_service.create_post(body)
    response_body["post_id"] = post_id
    return response_body, 201

@posts_controller_admin.route('/posts', methods=['GET'])
@auth.login_required
def fetch_posts():
    return admin_service.fetch_all_posts(), 200

@posts_controller_admin.route('/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def update_post(post_id):
    response_body = {"status": "success"}
    body = ""
    try:
        body = request.get_json()
    except KeyError as e:
        response_body["status"] = "failure"
        response_body["reason"] = "missing mandatory field, <post_text>"
        return response_body, 400

    try:
        admin_service.update_post(post_id, body)
    except ValueError as e:
        response_body["status"] = "failure"
        response_body["reason"] = str(e)
        return response_body, 400

    return response_body, 204

@posts_controller_admin.route('/posts/<int:post_id>', methods=['GET'])
@auth.login_required
def fetch_post(post_id):
    post = admin_service.fetch_post(post_id)
    if post is None:
        return {"status": "failure",
                "reason": "post id: {post_id} doesn't exist".format(post_id=post_id)}, 404
    else:
        return post, 200

# TODO find a way to get around this.
def create_app():
    app = Flask(__name__)
    app.register_blueprint(posts_controller_admin)

    return app