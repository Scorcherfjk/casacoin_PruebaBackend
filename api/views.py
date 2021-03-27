from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.http import HttpResponse
from api.models import Scraper
import json


class ScraperAPI(View):
    def get(self, *args, **kwargs):

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

        data = json.loads(self.request.body.decode('utf-8'))

        scraper = Scraper(
            currency=data['currency'],
            value=data['value'],
            frequency=data['frequency']
        )
        scraper.save()

        return HttpResponse(json.dumps(
            {
                "currency": scraper.currency,
                "value": scraper.value,
                "frequency": scraper.frequency,
            }
        ), content_type='application/json')

    def put(self, *args, **kwargs):

        data = json.loads(self.request.body.decode('utf-8'))

        scraper = Scraper.objects.get(id=data['id'])
        scraper.frequency = data['frequency']
        scraper.save()

        return HttpResponse(
            json.dumps(
                {
                    "scrapers": [
                        {
                            "currency": scraper.currency,
                            "frequency": scraper.frequency,
                        }
                    ]
                },
            ),
            content_type='application/json')

    def delete(self, *args, **kwargs):

        data = json.loads(self.request.body.decode('utf-8'))
        scraper = Scraper.objects.get(id=data['id'])
        scraper.delete()

        return HttpResponse(
            json.dumps(
                {
                    "scrapers": [
                        {
                            "currency": scraper.currency,
                            "frequency": scraper.frequency,
                        }
                    ]
                },
            ),
            content_type='application/json')
