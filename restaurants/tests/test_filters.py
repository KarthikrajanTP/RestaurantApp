from django.test import TestCase
from django.contrib.auth.models import User
from django_filters import FilterSet
from restaurants.models import Cuisine, Restaurant
from restaurants.filters import RestaurantFilter

class RestaurantFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cuisine1 = Cuisine.objects.create(name="Italian")
        self.cuisine2 = Cuisine.objects.create(name="Chinese")

        self.restaurant1 = Restaurant.objects.create(
            title="Restaurant A",
            rating=4.5,
            cost_for_two=1000.00,
            owner=self.user,
            location="New York",
            address="123 Street",
            timings="10 AM - 11 PM",
            food_type=Restaurant.VEG
        )
        self.restaurant1.cuisines.set([self.cuisine1])

        self.restaurant2 = Restaurant.objects.create(
            title="Restaurant B",
            rating=3.5,
            cost_for_two=500.00,
            owner=self.user,
            location="San Francisco",
            address="456 Street",
            timings="9 AM - 10 PM",
            food_type=Restaurant.NON_VEG
        )
        self.restaurant2.cuisines.set([self.cuisine2])

    def test_filter_by_city(self):
        filtered_qs = RestaurantFilter({'city': 'New York'}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.restaurant1)

    def test_filter_by_cost(self):
        filtered_qs = RestaurantFilter({'cost': 1000}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 2)
        filtered_qs = RestaurantFilter({'cost': 600}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.restaurant2)

    def test_filter_by_cuisine(self):
        filtered_qs = RestaurantFilter({'cuisines': self.cuisine1.id}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.restaurant1)

    def test_filter_by_food_type(self):
        filtered_qs = RestaurantFilter({'food_type': Restaurant.VEG}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.restaurant1)

    def test_filter_by_rating(self):
        filtered_qs = RestaurantFilter({'rating': 4}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.restaurant1)

    def test_ordering(self):
        filtered_qs = RestaurantFilter({'o': 'cost_for_two'}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.first(), self.restaurant2)
        filtered_qs = RestaurantFilter({'o': '-cost_for_two'}, queryset=Restaurant.objects.all()).qs
        self.assertEqual(filtered_qs.first(), self.restaurant1)
