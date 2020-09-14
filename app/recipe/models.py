from django.db import models


class Recipe(models.Model):
    """Recipe model"""
    name = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model"""
    name = models.TextField()
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name
