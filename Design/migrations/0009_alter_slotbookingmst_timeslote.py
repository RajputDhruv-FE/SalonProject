# Generated by Django 5.1.4 on 2025-02-09 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Design', '0008_slotbookingmst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slotbookingmst',
            name='TimeSlote',
            field=models.CharField(max_length=20),
        ),
    ]
