from flask import Blueprint, request, Flask
posts_controller_admin = Blueprint('users', __name__)
from service.admin_service import AdminService

admin_service = AdminService()


@posts_controller_admin.route('/posts', methods=['POST'])
def create_post():
    response_body = {"status": "success"}
    body = ""
    try:
        body = request.get_json()["post_text"]
    except KeyError as e:
        response_body["status"] = "failure"
        response_body["reason"] = "missing mandatory field, <post_text>"
        return response_body, 400

    admin_service.create_post(body)
    return response_body, 201

@posts_controller_admin.route('/posts', methods=['GET'])
def fetch_posts():
    return admin_service.fetch_all_posts(), 200

@posts_controller_admin.route('/posts/<int:post_id>', methods=['PUT'])
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