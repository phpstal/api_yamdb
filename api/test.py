from django.shortcuts import get_object_or_404

from .models import YamdbUser

def get_queryset(self, username):        
    user = get_object_or_404(YamdbUser, username=username)
    print(user)
    return user