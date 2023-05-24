from entity.post import Post

class PostsService:
    def fetch_all_visible_posts(self):
        visible_posts = Post.select().where(Post.visible == True)
        visible_post_json = []
        for post in visible_posts:
            visible_post_json.append({
                "id": post.id,
                "content": post.content,
                "created": post.created,
                "visible": post.visible,
                "deleted": post.deleted,
                "edited": post.edited
            })

        return visible_post_json

    def fetch_post(self, post_id):
        try:
            post = Post.get((Post.id == post_id) & (Post.visible == True))
            return {
                "id": post.id,
                "content": post.content,
                "created": post.created,
                "edited": post.edited
            }
        except Post.DoesNotExist:
            return []
