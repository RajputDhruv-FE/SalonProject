# Generated by Django 5.1.4 on 2025-01-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Design', '0002_servicemst_usermst'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citymst',
            options={'ordering': ['CityName']},
        ),
        migrations.AddField(
            model_name='usermst',
            name='Img',
            field=models.ImageField(default='images/default.jpg', upload_to=''),
        ),
    ]
