# Django imports
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

# Models
from api.models import Scraper

# Utils 
from datetime import datetime, timedelta
from sqlite3 import IntegrityError
import requests
import json

# version para entregar
import re

# solucion facil
from bs4 import BeautifulSoup


class ScraperAPI(View):
    def get(self, *args, **kwargs):
        """ Function to GET the Scrapers saved in the DB

        Input: N/A

        Output: 
        {
            "scrapers": [
                {
                    "created_at": "2021-03-27T02:41:55.456Z",
                    "currency": "Dogecoint",
                    "frequency": 60,
                    "id": 6,
                    "value": "$ 5",
                    "value_updated_at": "2021-03-27T02:53:05.817Z"
                }
            ]
        }

        """

        try:
            scrapers = Scraper.objects.values()
            data = []

            for reference in scrapers:

                scraper = Scraper.objects.get(id=reference['id'])

                now = datetime.now()
                updated_at = scraper.value_updated_at.replace(tzinfo=None)
                frequency = timedelta(minutes=scraper.frequency)

                interval = updated_at + frequency

                if interval < now:
                    search_currency = scraper.currency.strip().replace(' ', '-')
                    response = requests.get(
                'https://coinmarketcap.com/currencies/{}/'.format(search_currency)).text
                    soup = BeautifulSoup(response, features="html.parser")

                    price = soup.select_one('div[class*="priceValue"]').get_text()
                    scraper.value = price

                    scraper.save()
                
                data.append(scraper.toDict())


        except AttributeError:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. [{}] not found".format(data['currency']),
                    "example": "Please visit https://coinmarketcap.com/coins/",
                }
            }, indent=1),
                content_type='application/json')
        except requests.ConnectionError:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. Please retry",
                    "example": {
                        "currency": "Cardano",
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')
        except:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. Please retry",
                    "example": None,
                }
            }, indent=1),
                content_type='application/json')

        return HttpResponse(
            json.dumps(
                {
                    "scrapers": data
                },
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            ),
            content_type='application/json'
        )

    def post(self, *args, **kwargs):
        """
        Function to POST a new the Scrapers in the DB

        Input:
        {
            "currency": "Dogecoint",
            "frequency": 30
        }

        Output: 
        {
            "scraper": 
                {
                    "created_at": "2021-03-27T02:41:55.456Z",
                    "currency": "Dogecoint",
                    "frequency": 30,
                    "id": 6,
                    "value": "5",
                    "value_updated_at": "2021-03-27T02:53:05.817Z"
                }
        }

        """

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            search_currency = data['currency'].strip().replace(' ', '-')

            response = requests.get(
                'https://coinmarketcap.com/currencies/{}/'.format(search_currency)).text
            soup = BeautifulSoup(response, features="html.parser")

            price = soup.select_one('div[class*="priceValue"]').get_text()

            scraper = Scraper(
                currency=data['currency'],
                value=price,
                frequency=data['frequency']
            )

            scraper.save()

        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. Please send the correct payload.",
                    "example": {
                        "currency": "Cardano",
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')
        except requests.ConnectionError:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. Please retry",
                    "example": {
                        "currency": "Cardano",
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')
        except AttributeError:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. [{}] not found".format(data['currency']),
                    "example": "Please visit https://coinmarketcap.com/coins/",
                }
            }, indent=1),
                content_type='application/json')
        except IntegrityError:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. [{}] already exists".format(data['currency']),
                    "example": None,
                }
            }, indent=1),
                content_type='application/json')
        except:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. Please retry",
                    "example": {
                        "currency": "Cardano",
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')

        return HttpResponse(json.dumps(
            {
                "scraper": scraper.toDict()
            },
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder
        ), content_type='application/json')

    def put(self, *args, **kwargs):
        """ Function to PUT a new frequency in the selected 
        Scrapers from the DB

        Input:
        {
            "id": 1,
            "frequency": 30
        }

        Output: 
        {
            "scraper": 
                {
                    "created_at": "2021-03-27T02:41:55.456Z",
                    "currency": "Dogecoint",
                    "frequency": 30,
                    "id": 6,
                    "value": "5",
                    "value_updated_at": "2021-03-27T02:53:05.817Z"
                }
        }

        """

        # validate payload
        try:

            data = json.loads(self.request.body.decode('utf-8'))
            scraper = Scraper.objects.get(id=data['id'])
            scraper.frequency = data['frequency']
            scraper.save()

        except Scraper.DoesNotExist:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. id [{}] does not exists".format(data['id']),
                    "example": {
                        "id": 1,
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. Please send the correct payload.",
                    "example": {
                        "id": 1,
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')
        except:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. Please send the correct payload.",
                    "example": {
                        "id": 1,
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')

        return HttpResponse(
            json.dumps(
                {
                    "scraper": scraper.toDict()
                },
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            ),
            content_type='application/json')

    def delete(self, *args, **kwargs):
        """ Function to DELETE the selected Scrapers from the DB

        Input:
        {
            "id": 1,
        }

        Output: 
        {
            "scraper": 
                {
                    "created_at": "2021-03-27T02:41:55.456Z",
                    "currency": "Dogecoint",
                    "frequency": 30,
                    "id": 6,
                    "value": "5",
                    "value_updated_at": "2021-03-27T02:53:05.817Z"
                }
        }

        """

        try:

            data = json.loads(self.request.body.decode('utf-8'))

            scraper = Scraper.objects.get(id=data['id'])
            scraper.delete()

        except Scraper.DoesNotExist:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. id [{}] does not exists".format(data['id']),
                    "example": {'id': 1},
                }
            }, indent=1),
                content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({
                "error": {
                    "message": "An error has occurred. Please send the correct payload.",
                    "example": {'id': 1},
                }
            }, indent=1),
                content_type='application/json')
        except:
            return HttpResponseServerError(json.dumps({
                "error": {
                    "message": "An error has occurred. Please retry",
                    "example": {
                        "currency": "Cardano",
                        "frequency": 30
                    },
                }
            }, indent=1),
                content_type='application/json')

        return HttpResponse(
            json.dumps(
                {
                    "scraper": scraper.toDict()
                },
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            ),
            content_type='application/json')
