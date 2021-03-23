from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
