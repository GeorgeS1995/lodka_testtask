from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Category
from .serializers import CategoriesSerializer

# Create your views here.


class CategoriesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
