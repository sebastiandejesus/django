# Generated by Django 2.0.4 on 2018-05-13 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meallogger', '0009_auto_20180513_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
