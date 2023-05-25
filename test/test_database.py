import unittest
from dao.database import db


class TestDatabase(unittest.TestCase):

    def test_db_configured(self):
        self.assertIsNotNone(db)


if __name__ == '__main__':
    unittest.main()
