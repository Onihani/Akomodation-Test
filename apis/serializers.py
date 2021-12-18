from rest_framework import serializers
from home.models import Property, Category
from django.contrib.auth import get_user_model
User = get_user_model()


class TypeRelatedField(serializers.RelatedField):
    def to_representation(self, obj):
        return {
       
'category': obj.name }



class OwnerRelatedField(serializers.RelatedField):
    def to_representation(self, obj):
        return {
                  'name': obj.username, "telephone":obj.telephone, "email":obj.email }


class PropertySerializer(serializers.ModelSerializer):
    type = TypeRelatedField(queryset=Category.objects.all())
    owner = OwnerRelatedField(queryset=User.objects.all())
    class Meta:
        model = Property
        fields = ['title', 'description', 'image', 'date', 'price', 'location', 'type', 'owner']


