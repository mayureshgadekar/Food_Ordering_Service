# Generated by Django 2.1.15 on 2022-12-09 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0010_auto_20221209_1356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_page_display',
            old_name='emailid',
            new_name='r_emailid',
        ),
    ]
