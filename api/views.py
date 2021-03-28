# Django imports
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

# Models
from api.models import Scraper

# Utils
from datetime import datetime, timedelta
import requests
import json

# version para entregar
import re

# solucion facil
from bs4 import BeautifulSoup


class ScraperAPI(View):
    def get(self, *args, **kwargs):
        """GET the Scrapers saved in the DB

        Input: N/A

        Output: 
        {
            "scrapers": [
                {
                    "id": (int) scraper ID,
                    "created_at": (isoformat str),
                    "currency": (str) currency name,
                    "frequency": (int) job frequency in seconds,
                    "value": (float) currency price,
                    "value_updated_at": (isoformat str)
                }
            ]
        }

        Output error:
        { "error": (str) message }
        """

        try:
            scrapers = Scraper.objects.values()
            data = []

            for reference in scrapers:

                scraper = Scraper.objects.get(id=reference['id'])

                now = datetime.now()
                updated_at = scraper.value_updated_at.replace(tzinfo=None)
                frequency = timedelta(seconds=scraper.frequency)

                interval = updated_at + frequency

                if interval < now:
                    search_currency = scraper.currency.strip().replace(' ', '-')
                    response = requests.get(
                        'https://coinmarketcap.com/currencies/{}/'.format(search_currency)).text
                    soup = BeautifulSoup(response, features="html.parser")

                    price = soup.select_one(
                        'div[class*="priceValue"]').get_text()
                    scraper.value = float(price.lstrip('$').replace(',', '_'))

                    scraper.save()

                data.append(scraper.toDict())

        except AttributeError:
            return HttpResponseServerError(json.dumps({
                "error": "[{}] not found".format(scraper.currency)}),
                content_type='application/json')
        except requests.ConnectionError:
            return HttpResponseServerError(
                json.dumps({"error": "Connection error, please retry"}),
                content_type='application/json')
        except:
            return HttpResponseServerError(
                json.dumps({"error": "Please retry"}),
                content_type='application/json')

        return HttpResponse(
            json.dumps(
                {"scrapers": data},
                sort_keys=True, indent=1,
                cls=DjangoJSONEncoder
            ),
            content_type='application/json'
        )

    def post(self, *args, **kwargs):
        """POST a new the Scrapers in the DB

        Input:
        { 
            "currency": (str) currency name,
            "frequency": (int) job frequency in seconds 
        }

        Output: 
        {
            "id": (int) scraper ID,
            "created_at": (isoformat str),
            "currency": (str) currency name,
            "frequency": (int) job frequency in seconds
        }

        Output error:
        { "error": (str) message }
        """

        try:
            data = json.loads(self.request.body.decode('utf-8'))

            search_currency = data['currency'].strip().replace(' ', '-')
            response = requests.get(
                'https://coinmarketcap.com/currencies/{}/'.format(search_currency))

            if response.status_code == 404:
                raise ValueError()

            scraper = Scraper(
                currency=data['currency'],
                frequency=data['frequency']
            )
            scraper.save()

        except json.JSONDecodeError:
            return HttpResponseBadRequest(
                json.dumps({"error":  "Please send the correct payload"}),
                content_type='application/json')
        except requests.ConnectionError:
            return HttpResponseServerError(
                json.dumps({"error": "Connection error, please retry"}),
                content_type='application/json')
        except ValueError:
            return HttpResponseBadRequest(
                json.dumps(
                    {"error": '{0} not found in https://coinmarketcap.com/currencies/{0}/'.format(search_currency)}),
                content_type='application/json')
        except:
            return HttpResponseBadRequest(
                json.dumps(
                    {"error": "[{}] already exists".format(data['currency'])}),
                content_type='application/json')

        return HttpResponse(
            json.dumps({
                "id": scraper.id,
                "created_at": scraper.created_at,
                "currency": scraper.currency,
                "frequency": scraper.frequency
            }, cls=DjangoJSONEncoder),
            content_type='application/json')

    def put(self, *args, **kwargs):
        """PUT a new frequency in the selected Scraper from the DB

        Input:
        { "id": 1, "frequency": 30 }

        Output: 
        { "msg": (str) message }

        Output error:
        { "error": (str) message }
        """

        try:

            data = json.loads(self.request.body.decode('utf-8'))
            scraper = Scraper.objects.get(id=data['id'])
            scraper.frequency = data['frequency']
            scraper.save()

        except Scraper.DoesNotExist:
            return HttpResponseBadRequest(
                json.dumps(
                    {"error": "id [{}] does not exists".format(data['id'])}),
                content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponseBadRequest(
                json.dumps({"error": "Please send the correct payload"}),
                content_type='application/json')
        except:
            return HttpResponseServerError(
                json.dumps({"error":  "Please retry"}),
                content_type='application/json')

        return HttpResponse(
            json.dumps({"msg": "Scraper updated"}),
            content_type='application/json'
        )

    def delete(self, *args, **kwargs):
        """DELETE the selected Scrapers from the DB

        Input:
        { "id": 1 }

        Output: 
        { "msg": (str) message }

        Output error:
        { "error": (str) message }
        """

        try:

            data = json.loads(self.request.body.decode('utf-8'))

            scraper = Scraper.objects.get(id=data['id'])
            scraper.delete()

        except Scraper.DoesNotExist:
            return HttpResponseBadRequest(
                json.dumps(
                    {"error": "id [{}] does not exists".format(data['id'])}),
                content_type='application/json')
        except json.JSONDecodeError:
            return HttpResponseBadRequest(
                json.dumps({"error": "Please send the correct payload"}),
                content_type='application/json')
        except:
            return HttpResponseServerError(
                json.dumps({"error":  "Please retry"}),
                content_type='application/json')

        return HttpResponse(
            json.dumps({"msg": "Scraper deleted"}),
            content_type='application/json'
        )
