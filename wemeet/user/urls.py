from django.urls import path
from .views      import AccountSignUp, AccountLogin, AccountDetailModify, AccountCategory

urlpatterns = [
    path('/account/sign-up', AccountSignUp.as_view()), 
    path('/account/log-in', AccountLogin.as_view()), 
    path('/account', AccountDetailModify.as_view()),
    path('/account/category', AccountCategory.as_view())
]