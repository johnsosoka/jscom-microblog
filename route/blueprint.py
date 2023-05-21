from flask import Blueprint
from controller.testController import goodbye_world

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/goodbye', methods=['GET'])(goodbye_world)