# Generated by Django 5.1.2 on 2024-11-13 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_login_registration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Login',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
