# Generated by Django 3.2.8 on 2021-12-20 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0004_auto_20211031_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]