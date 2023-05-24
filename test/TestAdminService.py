import unittest
from unittest.mock import patch, Mock
from entity.post import Post
from service.admin_service import AdminService


class TestAdminService(unittest.TestCase):

    def setUp(self):
        self.admin_service = AdminService()

    def test_markdown_to_html_links(self):
        markdown_text = "Check out [OpenAI](https://www.openai.com)."
        expected_output = 'Check out <a href="https://www.openai.com">OpenAI</a>.'
        self.assertEqual(self.admin_service.markdown_to_html_links(markdown_text), expected_output)

    @patch.object(Post, 'create')
    def test_create_post(self, mock_create):
        post_content = "Check out [OpenAI](https://www.openai.com)."
        self.admin_service.create_post(post_content)
        mock_create.assert_called()

    @patch.object(Post, 'select')
    def test_fetch_all_posts(self, mock_select):
        mock_select.return_value = [Mock(content="Post 1", visible=True, created='2022-01-01', edited='2022-01-01')]
        posts = self.admin_service.fetch_all_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["content"], "Post 1")
        self.assertEqual(posts[0]["visible"], True)


if __name__ == '__main__':
    unittest.main()
