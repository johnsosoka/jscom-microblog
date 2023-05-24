from flask import Blueprint, request, Flask
posts_controller_admin = Blueprint('users', __name__)
from service.admin_service import AdminService

admin_service = AdminService()


@posts_controller_admin.route('/posts', methods=['POST'])
def create_post():
    print("inside POST")
    body = ""
    try:
        body = request.get_json()["post_text"]
    except KeyError as e:
        return "Bad Request"

    admin_service.create_post(body)
    print(body)
    return "Good bye. (POST)"

@posts_controller_admin.route('/posts', methods=['GET'])
def fetch_posts():
    return admin_service.fetch_all_posts()

# TODO find a way to get around this.
def create_app():
    app = Flask(__name__)
    app.register_blueprint(posts_controller_admin)

    return app