# Generated by Django 2.0.7 on 2019-01-11 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_auto_20190111_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]