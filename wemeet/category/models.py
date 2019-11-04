from django.db import models
from group.models import Groups
from user.models import Users

class Categories(models.Model):
    category_name = models.CharField(Users,max_length=50, null=False)
    mainphoto = models.CharField(max_length=4000, null=False)

    class Meta:
        db_table= 'categories'

class UsersCategories(models.Model):
    user_category = models.ForeignKey(Users, on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False, blank=False,unique=True)
    class Meta:
        db_table= 'userscategories'

class GroupsCategories(models.Model):
    group_category = models.ForeignKey(Groups, on_delete=models.CASCADE, primary_key=True, null=False, blank=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False, blank=False,unique=True)

    class Meta:
        db_table= 'groupscategories'
