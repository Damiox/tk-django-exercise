from django.test import TestCase

from recipe.models import Recipe, Ingredient


def sample_ingredient(recipe, name='Some ingredient'):
    """Create a sample ingredient for a recipe performing the associations"""
    ingredient = Ingredient.objects.create(name=name, recipe=recipe)
    recipe.ingredients.add(ingredient)
    return ingredient


def sample_recipe(name='Some recipe', description='Some description'):
    """Create a sample recipe"""
    return Recipe.objects.create(name=name, description=description)


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        recipe = sample_recipe(
            name='Only Cucumber',
            description='Just eat the ingredient :)'
        )
        ingredient = sample_ingredient(recipe, name='cucumber')
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        # note: do not read this test if you are vegan
        recipe = sample_recipe(
            name='Asado',
            description='Argentinian barbecue'
        )
        sample_ingredient(recipe, name='rib meat')
        sample_ingredient(recipe, name='flank steak')
        sample_ingredient(recipe, name='pork sausage')
        sample_ingredient(recipe, name='blood sausage')
        sample_ingredient(recipe, name='intestines')
        sample_ingredient(recipe, name='lettuce')

        self.assertEqual(str(recipe), recipe.name)

    def test_multiple_recipes_with_same_ingredients(self):
        """Test creating two recipes with same ingredients"""
        # the exercise allows different ingredient instances
        # with the same name
        recipe1 = sample_recipe()
        sample_ingredient(recipe1, name='eggs')
        sample_ingredient(recipe1, name='salt')
        recipe2 = sample_recipe()
        sample_ingredient(recipe2, name='eggs')
        sample_ingredient(recipe2, name='salt')

        recipe_counts = Recipe.objects.all().count()
        ingredient_counts = Ingredient.objects.all().count()

        self.assertEqual(recipe_counts, 2)
        self.assertEqual(ingredient_counts, 4)
