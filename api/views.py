from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.http import HttpResponse
from api.models import Scraper
import json


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

        data = Scraper.objects.values()

        return HttpResponse(
            json.dumps(
                {
                    "scrapers": [value for value in data]
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
            "currency": "Ethereum",
            "frequency": 30
        }

        Output: 
        {
            "scraper": 
                {
                    "created_at": "2021-03-27T02:41:55.456Z",
                    "currency": "Dogecoint",
                    "frequency": 60,
                    "id": 6,
                    "value": "5",
                    "value_updated_at": "2021-03-27T02:53:05.817Z"
                }
        }

        """

        data = json.loads(self.request.body.decode('utf-8'))

        scraper = Scraper(
            currency=data['currency'],
            value="0",
            frequency=data['frequency']
        )
        scraper.save()

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

        data = json.loads(self.request.body.decode('utf-8'))

        scraper = Scraper.objects.get(id=data['id'])
        scraper.frequency = data['frequency']
        scraper.save()

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

        data = json.loads(self.request.body.decode('utf-8'))
        scraper = Scraper.objects.get(id=data['id'])
        scraper.delete()

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
