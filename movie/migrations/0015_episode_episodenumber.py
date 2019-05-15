# Generated by Django 2.0.7 on 2019-01-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0014_auto_20190111_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='episodenumber',
            field=models.CharField(blank=True, choices=[('E1', 'Episode 1'), ('E2', 'Episode 2'), ('E3', 'Episode 3'), ('E4', 'Episode 4'), ('E5', 'Episode 5'), ('E6', 'Episode 6'), ('E7', 'Episode 7'), ('E8', 'Episode 8'), ('E9', 'Episode 9'), ('E10', 'Episode 10'), ('E11', 'Episode 11'), ('E12', 'Episode 12'), ('E13', 'Episode 13'), ('E14', 'Episode 14'), ('E15', 'Episode 15')], max_length=2, null=True),
        ),
    ]
