# Generated by Django 4.2 on 2023-04-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_category_categories_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Toys', 'Toys'), ('Stationary', 'Stationary'), ('', ''), ('', ''), ('', '')], max_length=64),
        ),
    ]