# Generated by Django 2.1.5 on 2019-01-25 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0021_auto_20190125_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
