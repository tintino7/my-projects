# Generated by Django 4.2 on 2023-04-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categories',
            field=models.CharField(default='Product', max_length=64),
        ),
    ]
