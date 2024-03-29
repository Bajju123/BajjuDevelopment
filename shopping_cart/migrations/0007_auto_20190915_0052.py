# Generated by Django 2.2 on 2019-09-14 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_profile'),
        ('shopping_cart', '0006_auto_20190915_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]
