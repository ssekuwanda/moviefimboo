# Generated by Django 2.1.5 on 2019-01-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0020_auto_20190125_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(upload_to='./media'),
        ),
    ]
