# tk-django-exercise

This repo is just an approach for the Django Rest Framework TK exercise

## Build

The following command will build the docker images:
```
docker-compose build
```

## Run tests

The following command will run the set of unit tests along with the linting:
```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

## Start the server

The following command will leave a container running so you can test the API through the Django Admin site:
```
docker-compose up
```

### Django Admin

First, create an admin account to access the admin site later:
```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

Once the server is running, you can access the admin site through the following URL: 
`http://127.0.0.1:8000/admin`
