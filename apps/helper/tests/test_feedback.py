from django.contrib.admin import AdminSite
from django.test import TestCase, Client
from django.urls import reverse

from apps.account.models import User
from apps.helper.admin import FeedbackModelAdmin
from apps.helper.forms import AuthorizeFeedbackForm
from apps.helper.models import Feedback
from apps.helper.views import FeedbackFAQView


class FeedbackTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username="test", email="test@gmail.com", password="test")
        self.model_admin = FeedbackModelAdmin(model=Feedback, admin_site=AdminSite())

    def test_str(self):
        obj = Feedback.objects.create(question="test-question", email="test@gmail.com")
        self.assertEqual(str(obj), f"Feedback #{obj.pk}")

    def test_page(self):
        url = reverse("helper")

        # Test unauthorized GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, FeedbackFAQView.as_view().__name__)

        self.client.login(username="test", password="test")

        # Test authorized GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test correct POST request
        response = self.client.post(url, {"question": "Hello world test question"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_form(self):
        # Test short question
        form = AuthorizeFeedbackForm(data={"question": "test"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("question"))

        # Test long question
        form = AuthorizeFeedbackForm(data={"question": "".join([str(i) for i in range(1000)])})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("question"))

        # Test correct question
        form = AuthorizeFeedbackForm(data={"question": "Test correct question test. Fine"})
        self.assertTrue(form.is_valid())

    def test_admin_save_model(self):
        object = Feedback.objects.create(question="test question", email="test@gmail.com")

        object.answer = "test answer"
        self.model_admin.save_model(obj=object, request=None, form=None, change=['answer'])
        object.refresh_from_db()
        self.assertTrue(object.answered)

    def test_admin_has_add_permission(self):
        self.assertFalse(self.model_admin.has_add_permission(None))

    def test_admin_get_readonly_fields(self):
        object_ = Feedback.objects.create(question="test question", email="test@gmail.com")
        object_answered = Feedback.objects.create(question="test question", email="test@gmail.com", answer="test", answered=True)

        self.assertFalse('answer' in self.model_admin.get_readonly_fields(None, object_))
        self.assertTrue('answer' in self.model_admin.get_readonly_fields(None, object_answered))
