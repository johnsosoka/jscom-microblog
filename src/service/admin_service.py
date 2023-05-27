from werkzeug.security import check_password_hash
from peewee import DoesNotExist
from entity.post import Post
from entity.user import User
import datetime
import re


class AdminService:

    def __init__(self):
        pass

    @staticmethod
    def markdown_to_html_links(text):
        def replace_link(match):
            text, url = match.groups()
            return f'<a href="{url}">{text}</a>'

        return re.sub(r'\[(.*?)\]\((.*?)\)', replace_link, text)

    def create_post(self, post_content):
        new_post = Post.create(
            content=self.markdown_to_html_links(post_content),
            created=datetime.datetime.now(),
            visible=True
        )
        return new_post.id

    def update_post(self, post_id, post_json: dict):
        try:
            post = Post.get(Post.id == post_id)
        except Post.DoesNotExist:
            raise ValueError("Post with ID does not exist.")
        # All other post fields should not be editable.
        if "content" in post_json:
            post.content = self.markdown_to_html_links(post_json["content"])
        if "visible" in post_json:
            post.visible = post_json["visible"]

        post.edited = datetime.datetime.now()
        post.save()

    def get_user_and_verify_password(self, username, password):
        user = User.get(User.username == username)
        if user is None or not self.verify_password(username, password):
            return None

        return user

    @staticmethod
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

    def fetch_all_posts(self, order_by="desc", page=1, per_page=10):
        """
        The admin fetch returns invisible posts + more timestamp details.
        """
        if order_by.lower() == "asc":
            all_posts = Post.select().order_by(Post.created.asc())
        else:  # Default is desc
            all_posts = Post.select().order_by(Post.created.desc())

        all_posts = all_posts.paginate(page, per_page)
        all_post_json = []

        for post in all_posts:
            all_post_json.append({
                "id": post.id,
                "content": post.content,
                "visible": post.visible,
                "created": post.created,
                "edited" : post.edited
            })

        return all_post_json


    def fetch_post(self, post_id):
        try:
            post = Post.get(Post.id == post_id)
            return {
                "id": post.id,
                "content": post.content,
                "visible": post.visible,
                "created": post.created,
                "edited": post.edited
            }
        except Post.DoesNotExist:
            return None
