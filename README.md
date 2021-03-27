# WebScraper

A django template for the backend technical test

## First Steps
Create and launch a virtualenv
```
virtualenv -p python3 .env
source .env/bin/active
```

Install the project requirements (within the virtualenv) and migrate to create the database.
```
pip install -r requirements.txt
python manage.py migrate
```

## Run Development Server
```
python manage.py runserver
```

## API Endpoints (payload and response)

### `/api/scrapers/`

#### `GET`
```
{
  "scrapers": [
    {
      "id": (int) scraper ID,
      "created_at": (isoformat str),
      "currency": (str) currency name,
      "frequency": (int) job frequency in seconds,
      "value": (float) currency price,
      "value_updated_at": (isoformat str)
    },
    ...
    ]
}
```
Example
```
{
  "scrapers": [
    {
      "id": 2,
      "created_at": "2020-06-30T22:16:41.375386+00:00",
      "currency": "bitcoin",
      "frequency": 60,
      "value": 9150.05,
      "value_updated_at": "2020-06-30T22:21:58.108506+00:00"
    },
    {
      "id": 3,
      "created_at": "2020-06-30T22:21:08.028843+00:00",
      "currency": "tether",
      "frequency": 100,
      "value": 0.999931,
      "value_updated_at": "2020-06-30T22:22:10.522852+00:00"
    }
  ]
}
```

#### `POST`
```
{
  "currency": (str) currency name as listed in CoinMarketCap,
  "frequency": (int) job frequency in seconds
}
```
200 Response
```
{
  "id": (int) scraper ID,
  "created_at": (isoformat str),
  "currency": (str) currency name,
  "frequency": (int) job frequency in seconds
}
```
400 Response
```
{"error": (str) message}
```
Example 
```
>>> curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"currency": "Dogecoin", "frequency": 25}' \
     http://localhost:8000/api/scrapers/

{
  "id": 5,
  "created_at": "2020-07-01T22:07:47.797137+00:00",
  "currency": "Dogecoin",
  "frequency": 25
}
```

Note: For valid currency names, visit: https://coinmarketcap.com/

#### `PUT`
```
{
  "id": (int) scraper ID,
  "frequency": (int) job new frequency in seconds
}
```
200 Response
```
{"msg": (str) message}
```
400 Response
```
{"error": (str) message}
```

Example 
```
>>> curl --header "Content-Type: application/json" \
     --request PUT \
     --data '{"id": 4, "frequency": 35}' \
     http://localhost:8000/api/scrapers/

{"msg": "Scraper updated"}
```

#### `DELETE`
```
{
  "id": (int) scraper ID,
}
```
200 Response
```
{"msg": (str) message}
```
400 Response
```
{"error": (str) message}
```

Example 
```
>>> curl --header "Content-Type: application/json" \
     --request DELETE \
     --data '{"id": 4}' \
     http://localhost:8000/api/scrapers/

{"msg": "Scraper deleted"}
```