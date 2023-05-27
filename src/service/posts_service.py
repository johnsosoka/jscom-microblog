from entity.post import Post


class PostsService:

    def fetch_all_visible_posts(self, order_by="desc", page=1, per_page=10):
        if order_by.lower() == "asc":
            visible_posts = Post.select().where(Post.visible == True).order_by(Post.created.asc())
        else:  # Default is desc
            visible_posts = Post.select().where(Post.visible == True).order_by(Post.created.desc())

        visible_posts = visible_posts.paginate(page, per_page)

        visible_post_json = []
        for post in visible_posts:
            visible_post_json.append({
                "id": post.id,
                "content": post.content,
                "created": post.created,
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
            return None
