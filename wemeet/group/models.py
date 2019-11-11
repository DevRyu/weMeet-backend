from django.db import models
from user.models import User
from category.models import Category
class Group(models.Model):

    name = models.CharField(max_length = 50, null = False)
    introduction = models.TextField(max_length = 5000, null = False)
    mainphoto = models.ImageField()
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)
    host = models.ForeignKey(User,on_delete = models.CASCADE,related_name='group')
    category = models.ManyToManyField(Category, through = "groupcategory")
    class Meta:
        db_table = 'group'
    
class GroupCategory(models.Model):
    
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    class Meta:
        db_table = 'groupcategory'
