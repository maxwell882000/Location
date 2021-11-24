# Generated by Django 3.2.8 on 2021-11-24 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialistApp', '0003_auto_20211102_1334'),
        ('commentApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentspecialist',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='specialistApp.specialist'),
        ),
        migrations.AlterField(
            model_name='reviewspecialist',
            name='specialist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='specialistApp.specialist'),
        ),
    ]
