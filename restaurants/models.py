from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    VEG = 'veg'
    NON_VEG = 'non-veg'
    VEGAN = 'vegan'

    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (VEGAN, 'Vegan'),
    ]

    title = models.CharField(max_length=200)
    rating = models.FloatField(default=0.0)
    cost_for_two = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    address = models.TextField()
    timings = models.CharField(max_length=200)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    photos = models.ImageField(upload_to='restaurant_photos/')
    cuisines = models.ManyToManyField(Cuisine)
    spotlight = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = average_rating
            self.save()
        else:
            self.rating = 0.0
            self.save()

class Dish(models.Model):
    VEG = 'veg'
    NON_VEG = 'non-veg'

    DISH_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
    ]

    restaurant = models.ForeignKey(Restaurant, related_name='menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.CharField(max_length=20, choices=DISH_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    visited = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.restaurant.title}'

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_restaurant_rating(sender, instance, **kwargs):
    restaurant = instance.restaurant
    restaurant.update_rating()
