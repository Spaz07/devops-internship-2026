import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")),
)

import app


class TestItemsHandlers(unittest.TestCase):
    @patch("app.get_table")
    def test_get_items_returns_items(self, mock_get_table):
        mock_get_table.return_value.scan.return_value = {
            "Items": [{"id": "1", "name": "Notebook"}]
        }

        result = app.get_items({}, None)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            json.loads(result["body"])["items"],
            [{"id": "1", "name": "Notebook"}],
        )

    @patch("app.get_table")
    def test_post_item_creates_item(self, mock_get_table):
        event = {"body": json.dumps({"name": "Notebook"})}

        result = app.create_item(event, None)

        self.assertEqual(result["statusCode"], 201)
        item = json.loads(result["body"])["item"]
        self.assertEqual(item["name"], "Notebook")
        self.assertTrue(item["id"])
        mock_get_table.return_value.put_item.assert_called_once_with(Item=item)

    def test_post_item_rejects_invalid_json(self):
        result = app.create_item({"body": "not-json"}, None)

        self.assertEqual(result["statusCode"], 400)

    def test_post_item_rejects_missing_name(self):
        result = app.create_item({"body": json.dumps({})}, None)

        self.assertEqual(result["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
