# Generated by Django 2.0.4 on 2018-05-07 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meallogger', '0003_auto_20180506_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='calories',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='items',
            field=models.CharField(max_length=60),
        ),
    ]
