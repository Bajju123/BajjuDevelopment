# Generated by Django 2.0.7 on 2019-08-02 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20190802_2023'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='productnew',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='productnew',
            name='category',
        ),
        migrations.DeleteModel(
            name='Productnew',
        ),
    ]