from django.urls import path
from .views      import AccountSignUp, AccountLogin, AccountDetailModify, AccountCategory

urlpatterns = [
    path('/sign-up', AccountSignUp.as_view()), 
    path('/login', AccountLogin.as_view()), 
    path('', AccountDetailModify.as_view()),
    path('/category', AccountCategory.as_view())
]
