from django.contrib import admin
from recipe import models


admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
