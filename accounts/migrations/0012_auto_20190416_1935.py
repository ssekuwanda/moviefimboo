# Generated by Django 2.1.5 on 2019-04-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_code_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code_payment',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
