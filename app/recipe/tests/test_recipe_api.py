from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def ingredient_detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_ingredient(recipe, name='Some ingredient'):
    """Create a sample ingredient for a recipe performing the associations"""
    ingredient = Ingredient.create(name=name, recipe=recipe)
    recipe.ingredients.add(ingredient)
    return ingredient


def sample_recipe(name='Some recipe', description='Some description'):
    """Create a sample recipe"""
    return Recipe.create(name=name, description=description)


class PublicRecipeApiTests(TestCase):
    """Test the publicly available API endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving all recipes"""
        recipe1 = sample_recipe(name='Basic vanilla cake')
        sample_ingredient(recipe1, name='eggs')
        sample_ingredient(recipe1, name='suggar')
        sample_ingredient(recipe1, name='more stuff')
        recipe2 = sample_recipe(name='Pumpkin pancakes')
        sample_ingredient(recipe2, name='eggs')
        sample_ingredient(recipe2, name='flour')
        sample_ingredient(recipe2, name='milk')
        sample_ingredient(recipe2, name='more stuff')
        sample_recipe(name='No food at all')

        recipes = Recipe.objects.all().order_by('name')
        RecipeSerializer(recipes, many=True)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, recipes.data)

    def test_retrieve_recipes_filtered_by_name_substr(self):
        """Test retrieving recipes filtered by name (substring)"""
        recipe1 = sample_recipe(name='Pizza')
        sample_ingredient(recipe1, 'dough')
        sample_ingredient(recipe1, 'cheese')
        sample_ingredient(recipe1, 'tomato')
        recipe2 = sample_recipe(name='Cake')
        sample_ingredient(recipe2, 'vanilla')
        recipe3 = sample_recipe(name='Pizza de Cancha')  # :)
        sample_ingredient(recipe3, 'dough')
        sample_ingredient(recipe3, 'tomato')

        res = self.client.get(RECIPES_URL, {'name': 'Pi'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['id'], recipe1.id)
        self.assertEqual(res.data[1]['id'], recipe3.id)

    def test_create_recipe(self):
        """Test creating new recipe"""
        payload = {'name': 'Basic vanilla cake',
                   'description': 'Bla bla bla',
                   'ingredients': [{'name': 'eggs'},
                                   {'name': 'suggar'},
                                   {'name': 'more stuff'}]}

        res = self.client.post(RECIPES_URL, payload)

        exists = Recipe.objects.filter(
            name=payload['name']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_partial_update_recipe(self):
        """Test updating (partially) a recipe"""
        orig_name = 'Some name'
        recipe = sample_recipe(name=orig_name, description='Some description')
        old_ingredient = sample_ingredient(recipe, 'Some ingredient')
        payload = {'description': 'Another description',
                   'ingredients': [{'name': 'Another ingredient'}]}

        url = ingredient_detail_url(recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()
        ingredients = recipe.ingredients.all()

        # should delete previous existing ingredient
        old_ingredient_exists = Ingredient.objects.filter(
            id=old_ingredient.id
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, orig_name)  # no update on this field
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0].name,
                         payload['ingredients'][0]['name'])
        self.assertFalse(old_ingredient_exists)  # old ingredient has been removed

    def test_full_update_recipe(self):
        """Test updating (fully) a recipe"""
        recipe = sample_recipe(name='Some name', description='Some description')
        old_ingredient = sample_ingredient(recipe, 'Some ingredient')
        payload = {'name': 'Another name',
                   'description': 'Another description',
                   'ingredients': [{'name': 'Another ingredient'}]}

        url = ingredient_detail_url(recipe.id)
        res = self.client.put(url, payload)

        recipe.refresh_from_db()
        ingredients = recipe.ingredients.all()

        # should delete previous existing ingredient
        old_ingredient_exists = Ingredient.objects.filter(
            id=old_ingredient.id
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0].name,
                         payload['ingredients'][0]['name'])
        self.assertFalse(old_ingredient_exists)  # old ingredient has been removed

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = sample_recipe()
        sample_ingredient(recipe, 'Some ingredient')

        url = ingredient_detail_url(recipe.id)
        res = self.client.delete(url)

        exists = Recipe.objects.filter(id=recipe.id).exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)
