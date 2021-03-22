from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainSerializer


class MyTokenObtainView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer
