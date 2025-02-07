from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurants.models import Restaurant, Cuisine, Review, Dish, BookmarkedRestaurant, VisitedRestaurant

class RestaurantListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.cuisine = Cuisine.objects.create(name='Italian')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG
        )
        self.restaurant.cuisines.add(self.cuisine)
    
    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_list.html')
        self.assertContains(response, 'Test Restaurant')

class RestaurantDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.cuisine = Cuisine.objects.create(name='Italian')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG
        )
        self.restaurant.cuisines.add(self.cuisine)
        self.review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=4.0,
            comment='Great food!'
        )
        self.bookmarked_restaurant = BookmarkedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        self.visited_restaurant = VisitedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        self.url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})

    def test_get_restaurant_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_detail.html')
        self.assertContains(response, 'Great food!')
        self.assertTrue(response.context['bookmarked'])
        self.assertTrue(response.context['visited'])

    def test_post_restaurant_detail_view(self):
        form_data = {'rating': 5.0, 'comment': 'Excellent!'}
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, self.url)
        updated_review = Review.objects.get(user=self.user, restaurant=self.restaurant)
        self.assertEqual(updated_review.rating, 5.0)
        self.assertEqual(updated_review.comment, 'Excellent!')

class DishListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG
        )
        self.dish = Dish.objects.create(
            restaurant=self.restaurant,
            name='Test Dish',
            price=10.00,
            dish_type=Dish.VEG
        )
        self.url = reverse('dish-list', kwargs={'pk': self.restaurant.pk})

    def test_dish_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dish_list.html')
        self.assertContains(response, 'Test Dish')

class SpotlightRestaurantsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Spotlight Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
            spotlight=True
        )
        self.url = reverse('spotlight_restaurants')

    def test_spotlight_restaurants_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_common_list.html')
        self.assertContains(response, 'Spotlight Restaurant')

class VisitedRestaurantViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Visited Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG
        )
        self.visited_restaurant = VisitedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        self.url = reverse('visited_restaurants')

    def test_visited_restaurant_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_common_list.html')
        self.assertContains(response, 'Visited Restaurant')

class BookmarkedRestaurantViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.restaurant = Restaurant.objects.create(
            title='Bookmarked Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG
        )
        self.bookmarked_restaurant = BookmarkedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        self.url = reverse('bookmarked_restaurants')

    def test_bookmarked_restaurant_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_common_list.html')
        self.assertContains(response, 'Bookmarked Restaurant')

class ToggleBookmarkViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
        )

    def test_should_add_bookmark_for_a_restaurant(self):
        url = reverse('toggle-bookmark', args=[self.restaurant.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'bookmarked': True})
        self.assertTrue(BookmarkedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_should_remove_bookmark_of_a_restaurant(self):
        BookmarkedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse('toggle-bookmark', args=[self.restaurant.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'bookmarked': False})
        self.assertFalse(BookmarkedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

class ToggleVisitViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.restaurant = Restaurant.objects.create(
            title='Test Restaurant',
            rating=4.5,
            cost_for_two=50.00,
            owner=self.user,
            location='Test Location',
            address='Test Address',
            timings='10 AM - 10 PM',
            food_type=Restaurant.VEG,
        )

    def test_should_add_visit_for_a_restaurant(self):
        url = reverse('toggle-visit', args=[self.restaurant.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'visited': True})
        self.assertTrue(VisitedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_should_remove_visit_of_a_restaurant(self):
        VisitedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse('toggle-visit', args=[self.restaurant.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'visited': False})
        self.assertFalse(VisitedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())