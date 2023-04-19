# Generated by Django 4.2 on 2023-04-16 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categories',
            field=models.CharField(default='Not specified', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='this_category', to='auctions.category'),
        ),
    ]