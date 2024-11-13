# Generated by Django 5.1.3 on 2024-11-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'new'), (2, 'in_progress'), (3, 'done')]),
        ),
    ]