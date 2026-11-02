"""API tests for the Accounts service."""

import unittest

from service import create_app
from service.models import db


class AccountRoutesTestCase(unittest.TestCase):
    """Exercise account CRUD behavior and response policies."""

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
                "FORCE_HTTPS": False,
                "CORS_ALLOWED_ORIGINS": ["http://localhost:3000"],
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_account(self, **overrides):
        """Create an account using the standard test payload."""
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "phone_number": "555-0100",
            "address": "1 Analytical Engine Way",
            "account_type": "standard",
        }
        payload.update(overrides)
        return self.client.post("/accounts", json=payload)

    def test_create_and_read_account(self):
        """Created accounts can be retrieved by their identifiers."""
        created = self.create_account()
        self.assertEqual(created.status_code, 201)
        account_id = created.get_json()["id"]

        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "ada@example.com")

    def test_create_requires_valid_name_and_email(self):
        """Creation rejects missing names and malformed email addresses."""
        missing_name = self.client.post(
            "/accounts", json={"email": "ada@example.com"}
        )
        invalid_email = self.create_account(email="not-an-email")

        self.assertEqual(missing_name.status_code, 400)
        self.assertEqual(invalid_email.status_code, 400)

    def test_duplicate_email_is_conflict(self):
        """The service rejects a duplicate email with HTTP 409."""
        self.assertEqual(self.create_account().status_code, 201)
        duplicate = self.create_account(name="Another Account")
        self.assertEqual(duplicate.status_code, 409)

    def test_list_accounts(self):
        """The collection endpoint returns the stored accounts."""
        self.create_account()
        response = self.client.get("/accounts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["accounts"]), 1)

    def test_update_account(self):
        """The update endpoint changes supplied account fields."""
        account_id = self.create_account().get_json()["id"]
        response = self.client.put(
            f"/accounts/{account_id}", json={"name": "Augusta King"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Augusta King")

    def test_delete_account(self):
        """The delete endpoint removes an account."""
        account_id = self.create_account().get_json()["id"]
        deleted = self.client.delete(f"/accounts/{account_id}")

        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(self.client.get(f"/accounts/{account_id}").status_code, 404)

    def test_missing_account_returns_not_found(self):
        """Read and delete return HTTP 404 for unknown identifiers."""
        self.assertEqual(self.client.get("/accounts/999").status_code, 404)
        self.assertEqual(self.client.delete("/accounts/999").status_code, 404)

    def test_json_content_type_is_required(self):
        """Mutating endpoints reject requests without JSON content type."""
        response = self.client.post("/accounts", data="{}")
        self.assertEqual(response.status_code, 415)

    def test_security_and_cors_headers(self):
        """Responses include the configured security and CORS headers."""
        response = self.client.get(
            "/health", headers={"Origin": "http://localhost:3000"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"], "http://localhost:3000"
        )


if __name__ == "__main__":
    unittest.main()
