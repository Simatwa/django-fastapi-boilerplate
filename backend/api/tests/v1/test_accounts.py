from unittest import TestCase

from fastapi.testclient import TestClient
from finance.models import Account, Transaction
from users.models import AuthToken, CustomUser

from api import app, v1_router
from api.tests import base_url, client, test_credentials
from api.tests.utils import get_model_example
from api.v1.account.models import (
    EditablePersonalData,
    PaymentAccountDetails,
    ResetPassword,
    SendMPESAPopupTo,
    TokenAuth,
)
from api.v1.models import ProcessFeedback


class TestCaseWithAuth(TestCase):
    def setUp(self):
        def get_token():
            resp = client.post(
                v1_router.url_path_for("User auth token"),
                data=test_credentials,
            )
            resp.raise_for_status()
            return TokenAuth(**resp.json()).access_token

        self.auth_token = get_token()
        self.auth_client = TestClient(
            app,
            base_url,
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )
        """Authenticated client"""
        self.user = CustomUser.objects.get(
            username=test_credentials["username"]
        )


class TestAccounts(TestCaseWithAuth):
    def test_fetch_profile(self):
        resp = self.auth_client.get(v1_router.url_path_for("Get user profile"))
        self.assertTrue(resp.is_success)

    def test_update_profile(self):
        resp = self.auth_client.patch(
            v1_router.url_path_for("Update user profile"),
            json=get_model_example(EditablePersonalData),
        )
        self.assertTrue(resp.is_success)

    def test_username_existence_check(self):
        for username, existence_status in [
            (test_credentials["username"], True),
            ("she73yw234x34339", False),
        ]:
            resp = client.get(
                v1_router.url_path_for("Check if username exists"),
                params=dict(username=username),
            )
            self.assertTrue(resp.is_success)
            self.assertEqual(
                ProcessFeedback(**resp.json()).detail, existence_status
            )

    def test_transactions(self):
        transaction_type = Transaction.TransactionType.DEPOSIT.value
        transaction_means = Transaction.TransactionMeans.OTHER.value
        transaction = Transaction.objects.create(
            user=self.user,
            type=transaction_type,
            means=transaction_means,
            amount=1000,
            notes="Automated test.",
        )
        resp = self.auth_client.get(
            v1_router.url_path_for("Financial transactions"),
            params=dict(type=transaction_type, means=transaction_means),
        )
        self.assertTrue(resp.is_success)
        self.assertTrue(bool(resp.json()))
        transaction.delete()

    def test_mpesa_payment_account_details(self):
        account = Account.objects.create(
            name="m-PeSA",
            paybill_number="247246",
            details="Automated test",
        )

        resp = self.auth_client.get(
            v1_router.url_path_for("M-Pesa payment account details")
        )
        self.assertTrue(resp.is_success)
        self.assertEqual(
            PaymentAccountDetails(**resp.json()).account_number,
            test_credentials["username"],
        )
        account.delete()

    def test_other_payment_account_details(self):
        resp = self.auth_client.get(
            v1_router.url_path_for("Other payment account details")
        )
        self.assertTrue(resp.is_success)

    def test_send_mpesa_payment_popup(self):
        Account.objects.create(
            name="m-PeSA",
            paybill_number="247246",
            details="Automated test",
        )
        resp = self.auth_client.post(
            v1_router.url_path_for("Send mpesa payment popup"),
            json=get_model_example(SendMPESAPopupTo),
        )
        self.assertTrue(resp.is_success)

    def test_send_password_reset_token(self):
        resp = client.get(
            v1_router.url_path_for("Send password reset token"),
            params=dict(identity=self.user.username),
        )
        self.assertTrue(resp.is_success)

    def test_reset_password(self):
        resp = client.get(
            v1_router.url_path_for("Send password reset token"),
            params=dict(identity=self.user.username),
        )
        self.assertTrue(resp.is_success)
        token = AuthToken.objects.get(user=self.user)
        resp = client.post(
            v1_router.url_path_for("Set new account password"),
            json=ResetPassword(
                username=self.user.username,
                new_password="_Clb03042003",
                token=token.token,
            ).model_dump(),
        )
        self.assertTrue(resp.is_success)
        self.user.set_password(test_credentials["password"])
        self.user.save()
