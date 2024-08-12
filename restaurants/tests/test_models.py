from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Cuisine, Restaurant, Photo, Dish, Review, Bookmark, Visit

class CuisineModelTests(TestCase):

    def setUp(self):
        self.cuisine = Cuisine.objects.create(name='Italian')

    def test_cuisine_str(self):
        self.assertEqual(str(self.cuisine), 'Italian')

class RestaurantModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cuisine = Cuisine.objects.create(name='Italian')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.restaurant.cuisines.add(self.cuisine)

    def test_restaurant_str(self):
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

    def test_update_rating_no_reviews(self):
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 0.0)

    def test_update_rating_with_reviews(self):
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=5.0,
            comment='Great place!'
        )
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 5.0)

class PhotoModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.photo = Photo.objects.create(
            restaurant=self.restaurant,
            image='path/to/image.jpg',
            description='Test photo'
        )

    def test_photo_str(self):
        self.assertEqual(str(self.photo), f'Photo for {self.restaurant.title}')

class DishModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.dish = Dish.objects.create(
            restaurant=self.restaurant,
            name='Test Dish',
            price=10.00,
            dish_type=Dish.VEG
        )

    def test_dish_str(self):
        self.assertEqual(str(self.dish), 'Test Dish')

class ReviewModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=4.0,
            comment='Great food!'
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), f'{self.user.username} - {self.restaurant.title}')

    def test_review_creation_updates_rating(self):
        self.assertEqual(self.restaurant.rating, 4.0)

    def test_review_deletion_updates_rating(self):
        self.review.delete()
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 0.0)

class BookmarkModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            bookmarked=True
        )

    def test_bookmark_str(self):
        self.assertEqual(str(self.bookmark), f'{self.user.username} - {self.restaurant.title}')

class VisitModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=0.0,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=False,
        )
        self.visit = Visit.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            visited=True
        )

    def test_visit_str(self):
        self.assertEqual(str(self.visit), f'{self.user.username} - {self.restaurant.title}')
