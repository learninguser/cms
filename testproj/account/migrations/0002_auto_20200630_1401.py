# Generated by Django 2.2.12 on 2020-06-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(blank=True, default='media/default.jpg', upload_to='account'),
        ),
    ]
