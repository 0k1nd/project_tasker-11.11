# Generated by Django 5.1.3 on 2024-11-12 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_rename_user_account_remove_project_editors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='editors',
            field=models.ManyToManyField(blank=True, null=True, related_name='editable_objects', to='myapp.account'),
        ),
    ]
