from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse("users:registration")
        self.data = {
            "first_name": "Andrei",
            "last_name": "Belevich",
            "username": "Test",
            "email": "test@gmail.com",
            "password1": "Aa270600",
            "password2": "Aa270600",
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["title"], "Store - Регистрация")
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_post_success(self):
        username = self.data.get("username")
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, data=self.data)

        # check user creation
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertFalse(User.objects.get(username=username).is_verified_email)

        # check creation EmailVerification object
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    def test_user_verification(self):
        self.client.post(self.path, data=self.data)
        user = User.objects.get(username=self.data.get("username"))
        email_verification = EmailVerification.objects.get(user=user)
        path = settings.DOMAIN_NAME + reverse("users:email_verification",
                                              kwargs={"email": user.email, "code": email_verification.code})
        self.client.get(path)
        user = User.objects.get(username=self.data.get("username"))

        self.assertTrue(user.is_verified_email)
