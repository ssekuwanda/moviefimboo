# Generated by Django 2.1.5 on 2019-04-25 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_code_payment_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_amount', models.PositiveIntegerField()),
                ('serie_amount', models.PositiveIntegerField()),
            ],
        ),
    ]
