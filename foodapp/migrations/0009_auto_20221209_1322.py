# Generated by Django 2.1.15 on 2022-12-09 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0008_user_page_display'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_page_display',
            old_name='name',
            new_name='r_emailid',
        ),
    ]
