from django.db import models

class Users(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_introduction = models.TextField(null=True)
    profile_photo = models.CharField(max_length=4000, null=True)
    sign_up_reason = models.CharField(max_length=60, null=True)
    birthday = models.DateField(null=True)
    
    class Meta:
        db_table='users'

class Genders(models.Model):

    id = models.ForeignKey('user.Users', on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    gender = models.CharField(max_length=1, null=True)

    class Meta:
        db_table='genders'
    
class Languages(models.Model):

    id = models.ForeignKey('user.Users', on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    language = models.CharField(max_length=4, null=True)
    
    class Meta:
        db_table='languages'
    