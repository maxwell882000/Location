# Generated by Django 3.2.8 on 2022-05-31 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specialistApp', '0007_auto_20220524_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialist',
            name='is_deactivated',
            field=models.BooleanField(default=True, verbose_name='Скрыть карточку специалиста'),
        ),
    ]
