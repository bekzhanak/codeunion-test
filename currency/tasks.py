from celery import shared_task
import requests
import xml.etree.ElementTree as ET
from .models import Currency


@shared_task(bind=True)
def update_currency(self):
    res = requests.get("http://www.nationalbank.kz/rss/rates_all.xml")
    if res.status_code != 200:
        raise RuntimeError("Currency request has failed")

    root = ET.fromstring(res.content.decode())

    currencies = {}
    for child in root[0].iter("item"):
        for title in child.iterfind("title"):
            name = title.text
        for desc in child.iterfind("description"):
            value = desc.text
        currencies[name] = value

    Currency.objects.bulk_create(
        [
            Currency(name=name, rate=value) for name, value in currencies.items()
        ],
        update_conflicts=True,
        update_fields=["rate"],
        unique_fields=["name"],
    )
