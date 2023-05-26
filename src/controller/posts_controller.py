from flask import Blueprint, jsonify, request
from service.posts_service import PostsService

posts_controller = Blueprint('posts', __name__)

posts_service = PostsService()


@posts_controller.route('/posts', methods=['GET'])
def fetch_posts():
    order_by = request.args.get('order_by', 'desc')
    page = int(request.args.get('page', '1'))
    per_page = int(request.args.get('per_page', '10'))
    posts = posts_service.fetch_all_visible_posts(order_by, page, per_page)
    return jsonify(posts), 200

@posts_controller.route('/posts/<int:post_id>', methods=['GET'])
def fetch_post(post_id):
    post = posts_service.fetch_post(post_id)
    if not post:
        return {"status": "failure",
                "reason": "post id: {post_id} doesn't exist".format(post_id=post_id)}, 404
    return [post], 200
