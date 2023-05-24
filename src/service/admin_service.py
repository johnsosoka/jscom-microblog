from entity.post import Post
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

    """
    The admin fetch returns invisible posts + more timestamp details.
    """
    def fetch_all_posts(self):
        all_posts = Post.select()
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