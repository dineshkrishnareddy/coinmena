# Coinmena Test 

Question:
Write an API using Django that fetches the price of BTC/USD from the alphavantage API every hour, and stores it on postgres. This API must be secured meaning that you need an API key to use it. There should be two endpoints: GET /api/v1/quotes - returns exchange rate and POST /api/v1/quotes which triggers force requesting of the price from alphavantage. The API & DB should be containerized using Docker as well.- Every part should be as simple as possible.
- The project should be committed to GitHub.
- The sensitive data such as alphavantage API key, should be passed from the .env “gitignored” file via environment variables.

## Setup
1. Clone the repo
```bash
git clone git@github.com:dineshkrishnareddy/coinmena.git
```

2. Run the docker container
```bash
cd coinmena
docker-compose up -d
```

## Generating/Getting API token
1. Generate API token 
```bash
curl -X POST -d "{\"key_name\": \"dummy\"}" http://localhost:8000/api/v1/api-key/
```

2. Get already created API token
```bash
curl -X GET http://localhost:8000/api/v1/api-key/?key_name=dummy
```

## Getting exchange rate
1. Get exchange rate 
```bash
curl -X POST -H "Authorization: Api-Key <API_KEY>" -d "{\"from_currency\": \"USD\", \"to_currency\": \"JPY\"}" http://localhost:8000/api/v1/quotes/
```

2. Get current exchange rate
```bash
curl -X GET -H "Authorization: Api-Key <API_KEY>" http://localhost:8000/api/v1/quotes/?from_currency=USD&to_currency=JPY
```

## Generating exchange rate every hour
We created a celery beat periodic task to populate exchange rate every hour.
We used redis as the message broker for celery

### How to run celery beat and celery worker manually
```bash
celery -A coinmena beat -l info
celery -A coinmena worker -l info
```
### NOTE
1. Without Authorization exchange rate API will return error. Authorization API_KEY can be generated as the above steps
2. `docker-compose` command will run celery tasks also along with web.
