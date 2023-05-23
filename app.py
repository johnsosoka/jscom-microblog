from flask import Flask
from controller.posts_admin_controller import posts_controller_admin

BASE_MICRO_BLOG_PATH = '/v1/micro-blog'
app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.register_blueprint(posts_controller_admin, url_prefix=BASE_MICRO_BLOG_PATH+'/admin')
    app.run(debug=True)
