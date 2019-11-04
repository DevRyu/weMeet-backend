from django.db import models
from user.models import Users
from group.models import Groups,GroupsUsers

#id로 줘도 되는건가? =Groups.id
class Events(models.Model):
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,)
    name = models.CharField(max_length=200, null=False)
    mainimage = models.CharField(max_length=4000, null=False)
    introduction = models.TextField(max_length=5000, null=False)
    findgroup = models.TextField(max_length=2000, null=False)
    lon = models.FloatField(max_length=50, null=False)
    lat = models.FloatField(max_length=50, null=False)
    limituser = models.IntegerField(max_length=1000, null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'events'

class EventsUsers(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    host_id = models.ForeignKey(GroupsUsers, on_delete=models.CASCADE, null=False, blank=False,unique=True)

    class Meta:
        db_table = 'eventsusers'
