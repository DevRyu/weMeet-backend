from django.urls import path
from .views      import AccountView, AccountSignUp,AccountLogin 

urlpatterns = [
    path('/account', AccountView.as_view()),  
    path('/account/sign-up', AccountSignUp.as_view()), 
    path('/account/log-in',AccountLogin.as_view()), 
]