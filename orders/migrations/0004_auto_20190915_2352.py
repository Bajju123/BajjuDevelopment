# Generated by Django 2.2 on 2019-09-15 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190915_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='username',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='username',
            new_name='user_name',
        ),
    ]
