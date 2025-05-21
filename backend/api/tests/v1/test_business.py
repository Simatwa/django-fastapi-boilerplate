from unittest import TestCase
from api.tests import client
from api.tests.utils import get_model_example
from api import v1_router
from api.v1.business.models import NewVisitorMessage, BusinessGallery, BusinessAbout
from external.models import About, Document
from management.models import AppUtility
from django.db import IntegrityError


class TestBusiness(TestCase):

    v1_router.url_path_for

    def test_about(self):
        about = About.objects.create(**get_model_example(BusinessAbout))
        about.save()
        resp = client.get(v1_router.url_path_for("Business information"))
        self.assertTrue(resp.is_success)
        about.delete()

    def test_visitor_message(self):
        resp = client.post(
            v1_router.url_path_for("New visitor message"),
            json=get_model_example(NewVisitorMessage),
        )
        self.assertTrue(resp.is_success)

    def test_business_galleries(self):
        resp = client.get(
            v1_router.url_path_for("Business galleries"),
        )
        self.assertTrue(resp.is_success)

    def test_feedbacks(self):
        resp = client.get(v1_router.url_path_for("Customers' feedback"))
        self.assertTrue(resp.is_success)

    def test_faqs(self):
        resp = client.get(v1_router.url_path_for("Frequently asked questions"))
        self.assertTrue(resp.is_success)

    def test_document(self):
        document_name = Document.DocumentName.TERMS_OF_USE.value
        document = Document.objects.create(
            name=document_name,
            content="",
        )
        delete_obj = True
        try:
            document.save()
        except IntegrityError:
            delete_obj = False
        resp = client.get(
            v1_router.url_path_for("Site document"), params=dict(name=document_name)
        )
        self.assertTrue(resp.is_success)
        if delete_obj:
            document.delete()

    def test_utility(self):
        utility_name = AppUtility.UtilityName.CURRENCY.value
        utility = AppUtility.objects.create(
            name=utility_name, description="", value="Ksh"
        )
        delete_obj = True
        try:
            utility.save()
        except IntegrityError:
            delete_obj = False
        resp = client.get(
            v1_router.url_path_for("App utilities"), params=dict(name=utility_name)
        )
        self.assertTrue(resp.is_success)
        if delete_obj:
            utility.delete()
