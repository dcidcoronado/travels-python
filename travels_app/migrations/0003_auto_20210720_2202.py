# Generated by Django 3.2.4 on 2021-07-21 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0001_initial'),
        ('travels_app', '0002_alter_travel_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel',
            name='user',
        ),
        migrations.AddField(
            model_name='travel',
            name='user',
            field=models.ManyToManyField(related_name='travels', to='login_registration_app.User'),
        ),
    ]
