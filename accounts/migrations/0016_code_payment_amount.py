# Generated by Django 2.1.5 on 2019-04-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='code_payment',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
