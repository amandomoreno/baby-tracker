# Generated by Django 3.1.6 on 2021-02-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='baby',
            name='doctors',
            field=models.ManyToManyField(to='main_app.Doctor'),
        ),
    ]
