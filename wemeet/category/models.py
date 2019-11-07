from django.db import models
class Category(models.Model):
    
    name = models.CharField(max_length=50, null=False)
    mainphoto = models.URLField(max_length=4000, null=False)

    class Meta:
        db_table= 'category'



