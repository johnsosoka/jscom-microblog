from flask import Blueprint, request, Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from base64 import b64decode, b64encode


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)
from service.admin_service import AdminService
admin_service = AdminService()

jwt = JWTManager()

posts_controller_admin = Blueprint('users', __name__)
auth = HTTPBasicAuth()

def is_base64(s):
    try:
        return b64encode(b64decode(s)).decode() == s
    except Exception:
        return False


@posts_controller_admin.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Missing JSON in request"}), 400

    # Extract and validate username and password
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Decode password base64 encoded password
    if not is_base64(password):
        return jsonify({"message": "password must be base64 encoded."}), 400
    password = b64decode(password).decode()

    # Fetch user from database
    user = admin_service.get_user_and_verify_password(username, password)

    if user is None:
        return jsonify({"message": "Bad username or password"}), 401

    # User is validated at this point
    access_token = create_access_token(identity=username)

    return jsonify(access_token=access_token), 200


#@auth.verify_password



@posts_controller_admin.route('/posts', methods=['POST'])
# @auth.login_required
@jwt_required()
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
# @auth.login_required
@jwt_required()
def fetch_posts():
    order_by = request.args.get('order_by', 'desc')
    page = int(request.args.get('page', '1'))
    per_page = int(request.args.get('per_page', '5'))

    return admin_service.fetch_all_posts(order_by, page, per_page), 200

@posts_controller_admin.route('/posts/<int:post_id>', methods=['PUT'])
# @auth.login_required
@jwt_required()
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
# @auth.login_required
@jwt_required()
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