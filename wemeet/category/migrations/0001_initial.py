# Generated by Django 2.2.6 on 2019-11-07 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mainphoto', models.URLField(max_length=4000)),
            ],
            options={
                'db_table': 'category',
            },
        ),
    ]
