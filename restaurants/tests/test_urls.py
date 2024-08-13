from django.test import TestCase
from django.urls import reverse, resolve
from restaurants.views import (
    RestaurantListView, RestaurantDetailView, DishListView,
    SpotlightRestaurantsView, VisitedRestaurantView, BookmarkedRestaurantView,
    ToggleBookmarkView, ToggleVisitView
)
from django.contrib.auth import get_user_model

User = get_user_model()

class URLTests(TestCase):
    def setUp(self):
        self.restaurant_id = 1
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_restaurant_list_url_resolves(self):
        url = reverse('restaurant-list')
        self.assertEqual(resolve(url).func.view_class, RestaurantListView)

    def test_spotlight_restaurants_url_resolves(self):
        url = reverse('spotlight_restaurants')
        self.assertEqual(resolve(url).func.view_class, SpotlightRestaurantsView)

    def test_visited_restaurants_url_resolves(self):
        url = reverse('visited_restaurants')
        self.assertEqual(resolve(url).func.view_class, VisitedRestaurantView)

    def test_bookmarked_restaurants_url_resolves(self):
        url = reverse('bookmarked_restaurants')
        self.assertEqual(resolve(url).func.view_class, BookmarkedRestaurantView)

    def test_restaurant_detail_url_resolves(self):
        url = reverse('restaurant-detail', args=[self.restaurant_id])
        self.assertEqual(resolve(url).func.view_class, RestaurantDetailView)

    def test_dish_list_url_resolves(self):
        url = reverse('dish-list', args=[self.restaurant_id])
        self.assertEqual(resolve(url).func.view_class, DishListView)

    def test_toggle_visit_url_resolves(self):
        url = reverse('toggle-visit', args=[self.restaurant_id])
        self.assertEqual(resolve(url).func.view_class, ToggleVisitView)

    def test_toggle_bookmark_url_resolves(self):
        url = reverse('toggle-bookmark', args=[self.restaurant_id])
        self.assertEqual(resolve(url).func.view_class, ToggleBookmarkView)

    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertEqual(resolve(url).func.__name__, 'index')
