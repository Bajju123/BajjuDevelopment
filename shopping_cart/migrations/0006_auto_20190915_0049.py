# Generated by Django 2.2 on 2019-09-14 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_profile'),
        ('shopping_cart', '0005_auto_20190915_0035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ManyToManyField(to='shop.Product'),
        ),
    ]
