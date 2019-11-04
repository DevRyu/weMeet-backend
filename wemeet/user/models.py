from django.db import models

class Genders(models.Model):

    gender = models.CharField(max_length=1, null=True)

    class Meta:
        db_table='genders'
    
class Languages(models.Model):

    language = models.CharField(max_length=2, null=True)
    
    class Meta:
        db_table='languages'
    
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
    gender = models.ForeignKey(Genders, on_delete   = models.SET_NULL, null = True, blank = True)
    language = models.ForeignKey(Languages, on_delete = models.SET_NULL, null=True, blank = True)    
    class Meta:
        db_table='users'