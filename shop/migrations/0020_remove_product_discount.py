# Generated by Django 2.2 on 2019-10-06 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
    ]
