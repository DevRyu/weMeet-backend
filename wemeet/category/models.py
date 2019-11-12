from django.db import models

class Category(models.Model):
    name       = models.CharField(max_length = 50, null   = False)
    main_photo = models.URLField(max_length  = 4000, null = False)

    class Meta:
        db_table= 'categories'
