This is the repository for codeunion's test project.

To run the project you need to have the docker installed:

```shell
docker-compose up --build
```

After the docker-compose started in another terminal run:

```shell
docker-compose run app python manage.py migrate
```

When project is running you can register via https://localhost:8000/auth/register
sending you username, email, and password in request body.

After you need to obtain you auth token via https://localhost:8000/auth/api-token-auth
by sending you username and password in request body. Further you can use this token in Authorization
header with Bearer keyword to authorize.

Program updates the actual rates from  http://www.nationalbank.kz/rss/rates_all.xml
every minute. You can access the rates via https://localhost:8000/currencies.
Or if you want a specific rate https://localhost:8000/currencies/<id>/ by passing the
id of the rate you want to get.

There is also the CLI to get and update the currencies.
To get the currencies:

```shell
python cli.py currencies
```

Running this will list all the currencies or if you want to get the specific one you can
pass the --id of the currency you want to get.

To update:

```shell
python cli.py update --id --rate
```

You need to pass the id and rate to update the currency.

You also can use --help to get the help.