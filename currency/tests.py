from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Currency
from django.contrib.auth.models import User
import random
import uuid


# Create your tests here.

def create_random_currencies(num_of_currencies: int) -> list[Currency]:
    currencies = []

    for i in range(num_of_currencies):
        currency = Currency.objects.create(name=str(uuid.uuid4()),
                                           rate=random.randint(0, 500))
        currencies.append(currency)
    return currencies


def create_user():
    user = User.objects.create(
        username='username',
        email='email',
    )
    user.set_password('password')
    user.save()
    return user


class CurrenciesListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.currencies = create_random_currencies(10)

    def test_unauthorized_currencies_fails(self):
        url = reverse("currencies")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 401)

    def test_authorized_currencies_succeeds(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("currencies")
        response = self.client.get(url)

        expected_currencies = self.currencies
        actual_currencies = response.data["results"]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(expected_currencies), len(actual_currencies))

        for i in range(len(expected_currencies)):
            currency_exp = expected_currencies[i]
            currency_res = actual_currencies[i]

            self.assertEqual(currency_exp.name, currency_res['name'])
            self.assertEqual(currency_exp.rate, currency_res['rate'])

    def test_authorized_currencies_pagination(self):
        currency = create_random_currencies(1)[0]
        self.client.force_authenticate(user=self.user)
        url = reverse("currencies")

        response = self.client.get(url, data={"page": "2"})
        actual_currencies = response.data["results"]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(actual_currencies), 1)
        self.assertEquals(actual_currencies[0]["name"], currency.name)
        self.assertEquals(actual_currencies[0]["rate"], currency.rate)


class CurrencyDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.currency = create_random_currencies(1)[0]
        self.currency_id = self.currency.id

    def test_unauthorized_currency_fails(self):
        url = reverse("currency_detail", kwargs={"id": self.currency_id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 401)

    def test_authorized_currency_succeeds(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("currency_detail", kwargs={"id": self.currency_id})

        response = self.client.get(url)
        actual_currency = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(actual_currency["name"], self.currency.name)
        self.assertEquals(actual_currency["rate"], self.currency.rate)

    def test_authorized_currency_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("currency_detail", kwargs={"id": self.currency_id - 1})

        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
