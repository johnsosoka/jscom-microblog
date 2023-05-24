from flask import Blueprint, jsonify
from service.posts_service import PostsService

posts_controller = Blueprint('posts', __name__)

posts_service = PostsService()

@posts_controller.route('/posts', methods=['GET'])
def fetch_posts():
    posts = posts_service.fetch_all_visible_posts()
    return jsonify(posts), 200

@posts_controller.route('/posts/<int:post_id>', methods=['GET'])
def fetch_post(post_id):
    post = posts_service.fetch_post(post_id)
    if not post:
        return post, 404
    return [post], 200
