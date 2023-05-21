from flask import Flask
from route.blueprint import blueprint
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    # db.create_all()  # Creates the table
    app.register_blueprint(blueprint)
    app.run(debug=True)
