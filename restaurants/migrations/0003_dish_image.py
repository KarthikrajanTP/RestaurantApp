# Generated by Django 5.0.7 on 2024-08-07 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_remove_restaurant_photos_alter_restaurant_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dish_photos/'),
        ),
    ]
