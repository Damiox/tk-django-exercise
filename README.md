# tk-django-exercise

This repo is just an approach for the Django Rest Framework TK exercise

## Exercise

Create a CRUD API with Django and DRF that allows you to CRUD recipes and add/delete ingredients to it.  Test it using postman or similar.

Entity details:
```
Recipe: Name, Description
Ingredient: Name, Recipe (ForeignKey) ← assume a given ingredient belongs only to one recipe, even if that means multiple Ingredient instances with the exact same name.
```

## API contract

### Example recipe creation
```
POST /recipes/
{
	“name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
}

Response:
{
	“id”: 1,
	“name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
}
```

### Example recipe list
```
GET /recipes/
[
    {
	“id”: 1,
      “name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
    }
]


Add search view by name substring:
GET /recipes/?name=Pi
[
    {
      “id”: 1,
	“name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
    }
]
```

### Example recipe edit
```
PATCH /recipes/1/
    {
	“name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “casa-tarradellas”}]
    }


Should delete the previous existing ingredients and put “casa-tarradellas” as only ingredient for recipe.

Response:
{
	“id”: 1,
	“name”: “Pizza”
	“description”: “Put it in the oven”,
	“ingredients”: [{“name”: “casa-tarradellas”}]
}
```

### Example recipe delete

```
DELETE /recipes/1/


Response:
HTTP 204 (NO CONTENT)


Should delete the targeted recipe AND its ingredients.
```

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
