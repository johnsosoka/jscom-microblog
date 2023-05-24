import unittest
from unittest.mock import patch, Mock, ANY
from service.admin_service import AdminService


class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.admin_service = AdminService()

    def test_markdown_to_html_links(self):
        markdown_text = '[John Sosoka](https://johnsosoka.com)'
        expected_html = '<a href="https://johnsosoka.com">John Sosoka</a>'
        result_html = self.admin_service.markdown_to_html_links(markdown_text)
        self.assertEqual(result_html, expected_html)

    @patch('service.admin_service.Post')
    def test_create_post(self, MockPost):
        markdown_text = '[John Sosoka](https://johnsosoka.com)'
        expected_html = '<a href="https://johnsosoka.com">John Sosoka</a>'
        self.admin_service.create_post(markdown_text)
        MockPost.create.assert_called_once_with(content=expected_html, created=ANY, visible=True)

    @patch('service.admin_service.Post')
    def test_fetch_all_posts(self, MockPost):
        mock_posts = [
            Mock(id=1, content="Hello, world!", visible=True, created="2023-05-19", edited="2023-05-19"),
            Mock(id=2, content="Another post", visible=True, created="2023-05-19", edited="2023-05-19"),
        ]
        MockPost.select.return_value = mock_posts

        expected_result = [
            {"id": 1, "content": "Hello, world!", "visible": True, "created": "2023-05-19", "edited": "2023-05-19"},
            {"id": 2, "content": "Another post", "visible": True, "created": "2023-05-19", "edited": "2023-05-19"},
        ]
        result = self.admin_service.fetch_all_posts()
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
