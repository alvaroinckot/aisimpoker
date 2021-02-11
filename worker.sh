if [ -f .env ]
then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

celery -A wsgi.celery worker