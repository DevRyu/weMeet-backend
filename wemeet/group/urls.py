from django.urls import path
from .views      import GroupMake,  GroupAllList, GroupCategoryList, GroupDetailView

urlpatterns = [
    path('', GroupAllList.as_view()),
    path('/group-make', GroupMake.as_view()),  
    path('/category/<int:pk>', GroupCategoryList.as_view()),
    path('/detail/<int:pk>', GroupDetailView.as_view()),
]