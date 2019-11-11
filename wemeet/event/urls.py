from django.urls import path
from .views      import EventCreate, AllEventListView, EventDetailView#, EventParticipant

urlpatterns = [
    path('/add', EventCreate.as_view()),
    path('', AllEventListView.as_view()),
    path('/detail', EventDetailView.as_view()),
    # path('/participant',EventParticipant.as_view()),
]