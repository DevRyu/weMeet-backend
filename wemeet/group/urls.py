from django.urls import path
from .views      import GroupMake,  GroupAllList, GroupCategoryList, GroupDetailView

urlpatterns = [
    path('/all', GroupList.as_view()),
    path('', Group.as_view()),  
    path('/category/<int:category_id>', GroupCategoryList.as_view()),
    path('/<int:group_id>', GroupDetailView.as_view()),
]
