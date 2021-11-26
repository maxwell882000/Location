# Generated by Django 3.2.8 on 2021-11-25 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locationApp', '0004_auto_20211125_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locationApp.locationcity', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='location',
            name='district',
            field=models.CharField(max_length=150, verbose_name='Район/Метро/Улица'),
        ),
        migrations.AlterField(
            model_name='location',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Локация активна'),
        ),
    ]