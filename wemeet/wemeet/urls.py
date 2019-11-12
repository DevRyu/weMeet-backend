from django.urls import path, include

urlpatterns = [
    path('user'    , include('user.urls')), 
    path('group'   , include('group.urls')), 
    path('category', include('category.urls')), 
    path('event'   , include('event.urls')), 
]

