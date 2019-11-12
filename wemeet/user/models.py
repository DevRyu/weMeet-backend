from django.db import models
from category.models import Category

class Gender(models.Model):
    gender = models.CharField(max_length=1, null=True)

    class Meta:
        db_table='gender'
        
class User(models.Model):
    name                 = models.CharField(max_length              = 50)
    email                = models.CharField(max_length              = 50, unique            = True)
    password             = models.CharField(max_length              = 300)
    updated_at           = models.DateTimeField(auto_now            = True)
    created_at           = models.DateTimeField(auto_now_add        = True)
    profile_introduction = models.TextField(null                    = True)
    profile_photo        = models.ImageField()
    gender               = models.ForeignKey(Gender, on_delete      = models.SET_NULL, null = True, blank = True)
    category             = models.ManyToManyField(Category, through = "usercategory")

    class Meta:
        db_table='user'
        
class UserCategory(models.Model):
    user     = models.ForeignKey(User, on_delete     = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
        
    class Meta:
        db_table= 'usercategory'
