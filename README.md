# AISimPoker.com

The poker player behavior simulator.

## How to run

### Docker

1. Install Docker and docker-compose
2. Run `docker-compose up -d`

### Locally

1. Setup Redis and Postgres servers, and update their addresses in the .env file
2. Run `pip i -r requirements.txt`
3. Start the API server: `flask run`
4. In another terminal, start the worker server: `celery -A wsgi.celery worker`
