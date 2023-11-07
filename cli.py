import click
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from currency.models import Currency


@click.group()
def cli():
    pass


@cli.command()
@click.option("--id", default=None, help="Id of the currency you want to get")
def currencies(id):
    if not id:
        queryset = Currency.objects.all()
        for currency in queryset:
            click.echo(f"{currency.id} {currency.name} {currency.rate}")
    else:
        currency = Currency.objects.get(id=id)
        if currency:
            click.echo(f"{currency.id} {currency.name} {currency.rate}")
        else:
            click.echo("There is no currency with this id")


@cli.command()
@click.option("--id", default=None, help="Id of the currency you want to update")
@click.option("--rate", default=None, help="Rate you want to set to the desired currency")
def update(id, rate):
    if not id:
        click.echo("Please provide the id of the currency you want to update")
    if not rate:
        click.echo("Please provide the rate you want to set to the desired currency")
    currency = Currency.objects.get(id=id)
    if currency:
        currency.rate = rate
        currency.save()
    else:
        click.echo("There is no currency with this id")


if __name__ == "__main__":
    cli()
