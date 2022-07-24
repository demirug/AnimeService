from django.test import TestCase

from apps.helper.models import FAQ


class HelperTestCase(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        obj = FAQ.objects.create(question="test-question", answer="test-answer")
        self.assertEqual(str(obj), obj.question)