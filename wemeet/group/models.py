from django.db import models
from user.models import Users
class Groups(models.Model):
    name = models.CharField(max_length=50, null=False)
    lon = models.FloatField(max_length=50, null=False)
    lat = models.FloatField(max_length=50, null=False)
    introduction = models.TextField(max_length=5000, null=False)
    mainphoto = models.CharField(max_length=4000, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'groups'

class GroupsUsers(models.Model):
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    name = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'groupsusers'