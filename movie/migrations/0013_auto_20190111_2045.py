# Generated by Django 2.0.7 on 2019-01-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_auto_20190111_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='season',
            field=models.CharField(blank=True, choices=[('S1', 'Season 1'), ('S2', 'Season 2'), ('S3', 'Season 3'), ('S4', 'Season 4'), ('S5', 'Season 5'), ('S6', 'Season 6')], max_length=2, null=True),
        ),
    ]
