# Generated by Django 2.1.5 on 2019-02-19 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190214_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='acc_amount',
            field=models.PositiveIntegerField(default=1000),
        ),
    ]
