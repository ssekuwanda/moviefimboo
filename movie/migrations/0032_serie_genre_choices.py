# Generated by Django 2.1.5 on 2019-03-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0031_auto_20190302_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='genre_choices',
            field=models.CharField(blank=True, max_length=122, null=True),
        ),
    ]
