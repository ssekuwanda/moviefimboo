# Generated by Django 2.1.5 on 2019-04-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20190426_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
