# Generated by Django 2.1.5 on 2019-02-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190219_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='acc_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
