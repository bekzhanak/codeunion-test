from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
import uuid


def create_user():
    user = User.objects.create(
        username='username',
        email='email',
    )
    user.set_password('password')
    user.save()
    return user


# Create your tests here.

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

    def test_register_succeeds(self):
        url = reverse("register")
        username = str(uuid.uuid4())
        email = "email@email.com"

        response = self.client.post(url, data={
            "username": username,
            "email": email,
            "password": str(uuid.uuid4())})

        self.assertEquals(response.status_code, 201)
        self.assertEquals(username, response.data["username"])
        self.assertEquals(email, response.data["email"])

    def test_register_fails(self):
        url = reverse("register")

        response = self.client.post(url, data={
            "email": "email@email.com",
            "password": str(uuid.uuid4())})

        self.assertEquals(response.status_code, 400)

    def test_obtain_token_succeeds(self):
        url = reverse("obtain_token")

        response = self.client.post(url, data={
            "username": self.user.username,
            "password": "password"
        })

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.data["token"])

    def test_obtain_token_fails(self):
        url = reverse("obtain_token")

        response = self.client.post(url, data={
            "username": uuid.uuid4(),
            "password": "password"
        })

        self.assertEquals(response.status_code, 400)
