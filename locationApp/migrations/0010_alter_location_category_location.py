# Generated by Django 3.2.8 on 2022-02-23 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specialistApp', '0006_alter_specialist_description'),
        ('locationApp', '0009_location_category_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='category_location',
            field=models.ManyToManyField(default=[], related_name='location', to='specialistApp.Category', verbose_name='Виды деятельности локации'),
        ),
    ]
