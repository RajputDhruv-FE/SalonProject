# Generated by Django 5.1.4 on 2025-01-01 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Design', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceMst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ServiceName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserMst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
                ('UserName', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=50)),
                ('PhoneNumber', models.CharField(max_length=10)),
                ('Password', models.CharField(max_length=20)),
                ('Usertype', models.CharField(max_length=10)),
                ('Status', models.CharField(max_length=10)),
            ],
        ),
    ]
