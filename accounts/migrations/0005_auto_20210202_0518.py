# Generated by Django 3.1.5 on 2021-02-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210201_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='dp.jpg', null=True, upload_to=''),
        ),
    ]