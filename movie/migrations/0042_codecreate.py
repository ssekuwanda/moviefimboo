# Generated by Django 2.1.5 on 2019-04-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0041_remove_movie_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeCreate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=6, null=True)),
                ('entered', models.BooleanField(default=False)),
            ],
        ),
    ]
