# Generated by Django 3.2.8 on 2022-02-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationApp', '0005_auto_20211125_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='name',
            field=models.CharField(default='Пусто', max_length=55, verbose_name='Название Картинки'),
        ),
    ]
