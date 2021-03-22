from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['password'] = user.password
        return token
