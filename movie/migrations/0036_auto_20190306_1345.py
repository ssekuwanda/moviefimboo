# Generated by Django 2.1.5 on 2019-03-06 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0035_auto_20190304_0530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='tag',
            new_name='tags',
        ),
    ]
