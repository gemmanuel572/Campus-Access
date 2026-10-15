import json
import os
import tempfile
import unittest

import request_manager as rm


class TestRequestManager(unittest.TestCase):

    def setUp(self):
        rm.requests.clear()

    def test_create_request(self):
        request = rm.create_request("F001", "student")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "student")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])

    def test_blank_fellow_id_rejected(self):
        with self.assertRaises(ValueError):
            rm.create_request(" ", "student")

    def test_invalid_card_type_rejected(self):
        with self.assertRaises(ValueError):
            rm.create_request("F001", "visitor-pass")

    def test_unique_ids(self):
        first = rm.create_request("F001", "student")
        second = rm.create_request("F002", "staff")

        self.assertEqual(first["id"], "A001")
        self.assertEqual(second["id"], "A002")

    def test_get_existing_request(self):
        rm.create_request("F001", "student")

        self.assertEqual(rm.get_request("A001")["fellow_id"], "F001")

    def test_get_unknown_request(self):
        self.assertIsNone(rm.get_request("A999"))

    def test_save_and_load(self):
        rm.create_request("F001", "visitor")

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
            path = file.name

        try:
            rm.save_requests(path)
            rm.requests.clear()
            rm.load_requests(path)

            self.assertEqual(len(rm.requests), 1)
            self.assertEqual(rm.requests[0]["id"], "A001")
        finally:
            os.unlink(path)

    def test_malformed_json_rejected(self):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False
        ) as file:
            file.write("{invalid json")
            path = file.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                rm.load_requests(path)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
