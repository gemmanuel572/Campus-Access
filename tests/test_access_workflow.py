import unittest

import request_manager as rm
import access_workflow as workflow


class TestAccessWorkflow(unittest.TestCase):

    def setUp(self):
        rm.requests.clear()
        rm.create_request("F001", "student")

    def test_approve_request(self):
        result = workflow.approve_request("A001", "M01")
        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["approved_by"], "M01")

    def test_blank_approver_rejected(self):
        before = rm.get_request("A001")

        with self.assertRaises(ValueError):
            workflow.approve_request("A001", " ")

        self.assertEqual(rm.get_request("A001"), before)

    def test_issue_before_approval_rejected(self):
        before = rm.get_request("A001")

        with self.assertRaises(ValueError):
            workflow.issue_request("A001")

        self.assertEqual(rm.get_request("A001"), before)

    def test_issue_after_approval(self):
        workflow.approve_request("A001", "M01")
        result = workflow.issue_request("A001")
        self.assertEqual(result["status"], "issued")

    def test_return_after_issue(self):
        workflow.approve_request("A001", "M01")
        workflow.issue_request("A001")
        result = workflow.return_request("A001")
        self.assertEqual(result["status"], "returned")

    def test_cannot_return_twice(self):
        workflow.approve_request("A001", "M01")
        workflow.issue_request("A001")
        workflow.return_request("A001")

        before = rm.get_request("A001")

        with self.assertRaises(ValueError):
            workflow.return_request("A001")

        self.assertEqual(rm.get_request("A001"), before)

    def test_cannot_issue_twice(self):
        workflow.approve_request("A001", "M01")
        workflow.issue_request("A001")

        before = rm.get_request("A001")

        with self.assertRaises(ValueError):
            workflow.issue_request("A001")

        self.assertEqual(rm.get_request("A001"), before)

    def test_unknown_request_rejected(self):
        with self.assertRaises(ValueError):
            workflow.approve_request("A999", "M01")


if __name__ == "__main__":
    unittest.main()
