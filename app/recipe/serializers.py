from django.utils.translation import gettext as _

from rest_framework import serializers

from recipe.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""
    # not allowing recipes with empty ingredients for now
    ingredients = IngredientSerializer(
        many=True, allow_empty=False,
        error_messages={
            'required': _('You have to specify ingredients for your recipe')
        }
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create operation for nested ingredients"""
        ingredients_data = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        # adding the ingredients
        for ingr_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingr_data)
        return recipe

    def update(self, instance, validated_data):
        """Update operation for nested ingredients"""
        ingredients_data = validated_data.pop('ingredients', None)
        recipe = super().update(instance, validated_data)
        if ingredients_data:
            # note: any previous ingredient is re-added again
            #       for simplicity at this point
            Ingredient.objects.filter(recipe=recipe).delete()
            for ingr_data in ingredients_data:
                Ingredient.objects.create(recipe=recipe, **ingr_data)
        return recipe
