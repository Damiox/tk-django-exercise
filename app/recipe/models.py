from django.db import models


class Recipe(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4096)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient object"""
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
