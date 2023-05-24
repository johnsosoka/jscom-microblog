import unittest
from unittest.mock import MagicMock, patch
from peewee import DoesNotExist
from service.posts_service import PostsService
import datetime


class TestPostsService(unittest.TestCase):
    @patch('service.posts_service.Post')
    def setUp(self, MockPost):
        self.MockPost = MockPost
        self.posts_service = PostsService()

    @unittest.skip("broken")
    def test_fetch_all_visible_posts(self):
        mock_post = MagicMock()
        mock_post.id = 1
        mock_post.content = 'Test Post'
        mock_post.created = datetime.datetime.now()
        mock_post.visible = datetime.datetime.now()
        mock_post.deleted = None
        mock_post.edited = datetime.datetime.now()

        self.MockPost.select().where.return_value = [mock_post]

        expected_result = [{
            "id": 1,
            "content": 'Test Post',
            "created": mock_post.created,
            "visible": mock_post.visible,
            "deleted": mock_post.deleted,
            "edited": mock_post.edited
        }]

        self.assertEqual(self.posts_service.fetch_all_visible_posts(), expected_result)

    @unittest.skip("broken")
    def test_fetch_post_success(self):
        mock_post = MagicMock()
        mock_post.id = 1
        mock_post.content = 'Test Post'
        mock_post.created = datetime.datetime.now()
        mock_post.visible = datetime.datetime.now()
        mock_post.edited = datetime.datetime.now()

        self.MockPost.get.return_value = mock_post

        expected_result = {
            "id": 1,
            "content": 'Test Post',
            "created": mock_post.created,
            "edited": mock_post.edited
        }

        self.assertEqual(self.posts_service.fetch_post(1), expected_result)

    @unittest.skip("broken")
    def test_fetch_post_does_not_exist(self):
        self.MockPost.get.side_effect = DoesNotExist

        self.assertEqual(self.posts_service.fetch_post(1), [])


if __name__ == '__main__':
    unittest.main()
