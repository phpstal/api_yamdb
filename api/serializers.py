  
from rest_framework import serializers, exceptions

from .models import (
    Comment, Review
)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=author, title_id=title_id).exists():
                raise exceptions.ValidationError('Отзыв уже существует')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
