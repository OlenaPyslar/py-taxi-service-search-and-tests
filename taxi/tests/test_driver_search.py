from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()
class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1",
            license_number="TRT12345"
        )
        self.client.force_login(self.user)
        User.objects.create_user(username='john', password='pass', license_number="TER12345")
        User.objects.create_user(username='jane', password='pass', license_number="TST34567")
        User.objects.create_user(username='doe', password='pass', license_number="TST23456")

    def test_search_by_username_returns_matching_users(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=ja")

        self.assertEqual(response.status_code, 200)
        object_list = response.context['object_list']
        self.assertTrue(all('ja' in u.username for u in object_list))
        self.assertFalse(any(u.username == 'john' for u in object_list))