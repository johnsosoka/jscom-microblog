import unittest
from unittest.mock import patch
from flask import json
from controller.posts_admin_controller import create_app


class TestPostsAdminController(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('controller.posts_admin_controller.admin_service.create_post')
    def test_create_post(self, mock_create_post):
        response = self.client.post('/posts', data=json.dumps({"post_text": "Hello, World!"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        mock_create_post.assert_called_with("Hello, World!")

    @patch('controller.posts_admin_controller.admin_service.fetch_all_posts')
    def test_fetch_posts(self, mock_fetch_all_posts):
        mock_fetch_all_posts.return_value = [
            {"content": "Post 1", "visible": True, "created": '2022-01-01', "edited": '2022-01-01'}
        ]
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [{"content": "Post 1", "visible": True, "created": '2022-01-01', "edited": '2022-01-01'}])

if __name__ == '__main__':
    unittest.main()