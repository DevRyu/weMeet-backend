from django.urls import path
from .views      import AccountSignUp,AccountLogin 

urlpatterns = [
    path('/account/sign-up', AccountSignUp.as_view()), 
    path('/account/log-in',AccountLogin.as_view()), 
]