from rest_framework import serializers, exceptions

from .models import YamdbUser, Genre, Category, Title, Review, Comment


class YamdbUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        extra_kwargs = {'username': {'required': True}}
        model = YamdbUser


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['view'].action != 'create':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise exceptions.ValidationError('Отзыв уже был оставлен.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
        model = Comment


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = YamdbUser


class GetTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.StringRelatedField(many=False)

    def validate_email(self, value):
        if not YamdbUser.objects.filter(email=value).exists():
            return serializers.ValidationError('You cant follow yourself')
        return value

    class Meta:
        fields = ('email', 'confirmation_code',)
        read_only_fields = ['email']
        extra_kwargs = {'confirmation_code': {'required': True}}
        model = YamdbUser
