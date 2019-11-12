from django.db import models
from user.models import User
from group.models import Group, GroupCategory
from django.core.validators import MaxValueValidator

class Location(models.Model):
    name = models.CharField(max_length=30)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    address = models.CharField(max_length=50)

    class Meta:
        db_table = 'location'

class Event(models.Model):
    title = models.CharField(max_length = 200)
    mainimage = models.ImageField()
    introduction = models.TextField(max_length = 5000)
    findlocation = models.CharField(max_length = 2000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit_user = models.IntegerField()
    attend_status = models.IntegerField(null = True)
    user = models.ManyToManyField(User, through = "EventUser")
    location = models.OneToOneField(Location, on_delete = models.CASCADE)
    group = models.ForeignKey(Group,on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'event'

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    participant = models.BooleanField(null=True)
    class Meta:
        db_table = 'eventuser'


