# Generated by Django 2.1.5 on 2019-02-14 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0024_auto_20190125_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=122, null=True)),
                ('font', models.TextField(blank=True, null=True)),
                ('text_color', models.CharField(blank=True, max_length=122, null=True)),
                ('back_ground_image1', models.ImageField(blank=True, null=True, upload_to='./media/bg_image')),
                ('back_ground_image2', models.ImageField(blank=True, null=True, upload_to='./media/bg_image')),
            ],
        ),
    ]