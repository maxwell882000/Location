# Generated by Django 3.2.8 on 2022-02-20 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationApp', '0007_alter_images_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='name',
            field=models.CharField(blank=True, default='', max_length=55, verbose_name='Название Картинки'),
        ),
    ]
