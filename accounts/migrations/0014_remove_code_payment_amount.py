# Generated by Django 2.1.5 on 2019-04-25 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_code_payment_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code_payment',
            name='amount',
        ),
    ]
