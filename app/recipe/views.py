from rest_framework import viewsets

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """Return recipes - filtered by name substring (optionally)"""
        queryset = self.queryset
        filter_name = self.request.query_params.get('name')
        if filter_name:
            queryset = queryset.filter(name__contains=filter_name)
        return queryset.order_by('id')
