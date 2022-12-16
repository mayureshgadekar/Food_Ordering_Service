# Generated by Django 2.1.15 on 2022-12-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='insert_resdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_emailid', models.CharField(max_length=100)),
                ('r_password', models.CharField(max_length=100)),
                ('r_name', models.CharField(max_length=100)),
                ('r_phone_number', models.IntegerField()),
                ('r_address', models.CharField(max_length=100)),
                ('r_city', models.CharField(max_length=100)),
                ('r_country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='signin_userdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
