from rest_framework import serializers

from .models import YamdbUser


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
