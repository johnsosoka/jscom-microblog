from flask import Flask
from controller.posts_admin_controller import posts_controller_admin, jwt
from controller.posts_controller import posts_controller


BASE_MICRO_BLOG_PATH = '/v1/micro-blog'
app = Flask(__name__)

# TODO read from yml config
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt.init_app(app)

@app.route("/healthcheck")
def healthcheck():
    return "Good.", 200


if __name__ == '__main__':
    app.register_blueprint(posts_controller_admin, url_prefix=BASE_MICRO_BLOG_PATH+'/admin')
    app.register_blueprint(posts_controller, url_prefix=BASE_MICRO_BLOG_PATH)
    app.run(debug=True)
