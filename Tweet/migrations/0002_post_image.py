# Generated by Django 5.0.4 on 2024-07-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tweet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='postPictures/'),
        ),
    ]
