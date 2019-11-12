from django.urls import path
from .views      import EventCreate, AllEventListView, EventDetailView#, EventParticipant

urlpatterns = [
    path('/<int:group_id>', Event.as_view()),
    path('', EventListView.as_view()),
    path('/<int:event_id>', EventDetailView.as_view())
]
