# Generated by Django 2.1.15 on 2022-12-12 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0012_insert_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='insert_cart',
            name='r_name',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]