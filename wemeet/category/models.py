from django.db import models
class Categories(models.Model):
    name = models.CharField(max_length=50, null=False)
    mainphoto = models.CharField(max_length=4000, null=False)

    class Meta:
        db_table= 'categories'



