from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurants.models import Cuisine, Restaurant, Photo, Dish, Review
from django.utils.crypto import get_random_string
from random import randint, choice

class Command(BaseCommand):
    help = 'Add sample data to the database'

    def handle(self, *args, **kwargs):
        # Create some cuisines
        cuisines = ['Italian', 'Chinese', 'Mexican', 'Indian', 'Thai', 'French']
        cuisine_objects = [Cuisine.objects.get_or_create(name=cuisine)[0] for cuisine in cuisines]

        # Create a test user
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('password123')
            user.save()

        # Create some restaurants
        for _ in range(20):
            restaurant = Restaurant.objects.create(
                title=f'Restaurant {get_random_string(5)}',
                rating=round(randint(1, 50) / 10, 1),
                cost_for_two=randint(20, 100),
                owner=user,
                location=f'Location {get_random_string(5)}',
                address=f'Address {get_random_string(15)}',
                timings='10:00 AM - 10:00 PM',
                food_type=choice([Restaurant.VEG, Restaurant.NON_VEG, Restaurant.VEGAN]),
                spotlight=choice([True, False])
            )
            # Add cuisines to restaurant
            restaurant.cuisines.add(*cuisine_objects[:randint(1, 3)])

            # Add some photos
            for _ in range(randint(1, 5)):
                Photo.objects.create(
                    restaurant=restaurant,
                    image='restaurant_photos/filter_coffee.jpg',
                    description=f'Photo for {restaurant.title}'
                )

            # Add some dishes
            for _ in range(randint(1, 5)):
                Dish.objects.create(
                    restaurant=restaurant,
                    name=f'Dish {get_random_string(5)}',
                    price=randint(5, 50),
                    dish_type=choice([Dish.VEG, Dish.NON_VEG])
                )

            # Add some reviews
            for _ in range(randint(1, 5)):
                Review.objects.create(
                    user=user,
                    restaurant=restaurant,
                    rating=round(randint(1, 50) / 10, 1),
                    comment=f'Comment {get_random_string(15)}',
                    visited=choice([True, False]),
                    bookmarked=choice([True, False])
                )

        self.stdout.write(self.style.SUCCESS('Successfully added sample data'))
