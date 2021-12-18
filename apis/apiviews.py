
from django.db.models import Q
from .serializers import PropertySerializer
from rest_framework import generics
from home.models import Property

class PropertyView(generics.ListAPIView):
#    model = Property
    serializer_class = PropertySerializer
    def get_queryset(self):
        return Property.objects.filter(type__name=self.kwargs['type']).all()

class SearchView(generics.ListAPIView):
    serializer_class = PropertySerializer
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        return Property.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

class ParamView(generics.ListAPIView):
    serializer_class = PropertySerializer
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is None:
            return Property.objects.all()
        return Property.objects.all()[:int(query)]

