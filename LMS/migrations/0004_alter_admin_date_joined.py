# Generated by Django 4.1.1 on 2022-09-10 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0003_admin_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
