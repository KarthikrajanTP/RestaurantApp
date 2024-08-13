from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Restaurant, Cuisine, Review, Dish, BookmarkedRestaurant, VisitedRestaurant
from .filters import RestaurantFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.http import JsonResponse

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['cuisines'] = Cuisine.objects.all()
        context['food_types'] = Restaurant.FOOD_TYPE_CHOICES
        context['ratings'] = [1, 2, 3, 4, 5]
        context['cost_ranges'] = [200, 500, 1000, 2000, 3000]
        return context

class RestaurantDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        reviews = restaurant.reviews.all()

        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        user_review = reviews.filter(user=request.user).first()
        review_form = self._is_update_review_form(user_review)

        bookmarked = BookmarkedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists()
        visited = VisitedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists()

        # Adding range for stars
        star_range = range(1, 6)
        user_rating = user_review.rating if user_review else 0

        return render(request, 'restaurant_detail.html', {
            'restaurant': restaurant,
            'page_obj': page_obj,
            'review_form': review_form,
            'user_review': user_review,
            'bookmarked': bookmarked,
            'visited': visited,
            'star_range': star_range,
            'user_rating': user_rating,
        })

    def post(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        user_review = restaurant.reviews.filter(user=request.user).first()
        form = self._is_update_review_form(user_review, request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()

            return redirect('restaurant-detail', pk=pk)

        reviews = restaurant.reviews.all()
        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        bookmarked = BookmarkedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists()
        visited = VisitedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists()

        return render(request, 'restaurant_detail.html', {
            'restaurant': restaurant,
            'page_obj': page_obj,
            'review_form': form,
            'user_review': user_review,
            'bookmarked': bookmarked,
            'visited': visited,
            'star_range': range(1, 6),
            'user_rating': form.cleaned_data.get('rating', 0),
        })

    def _is_update_review_form(self, user_review=None, data=None):
        if user_review:
            return ReviewForm(data, instance=user_review)
        else:
            return ReviewForm(data)


class DishListView(ListView):
    model = Dish
    template_name = 'dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 9

    def get_queryset(self):
        return Dish.objects.filter(restaurant_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        context['restaurant'] = restaurant
        return context
    
class SpotlightRestaurantsView(ListView):
    model = Restaurant
    template_name = 'restaurant_common_list.html'
    context_object_name = 'restaurants'
    page_title = 'Spotlight Restaurants'

    def get_queryset(self):
        return Restaurant.objects.filter(spotlight=True)

class VisitedRestaurantView(ListView):
    model = Restaurant
    context_object_name = 'restaurants'
    template_name = 'restaurant_common_list.html'
    page_title = 'Visited Restaurants'

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(visits__user=user).distinct()
    
class BookmarkedRestaurantView(ListView):
    model = Restaurant
    context_object_name = 'restaurants'
    template_name = 'restaurant_common_list.html'
    page_title = 'Bookmarked Restaurants'

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(bookmarks__user=user).distinct()


class ToggleVisitView(View):
    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if VisitedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists():
            VisitedRestaurant.objects.filter(user=request.user, restaurant=restaurant).delete()
            visited = False
        else:
            VisitedRestaurant.objects.create(user=request.user, restaurant=restaurant)
            visited = True
        return JsonResponse({'success': True, 'visited': visited})

class ToggleBookmarkView(View):
    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if BookmarkedRestaurant.objects.filter(user=request.user, restaurant=restaurant).exists():
            BookmarkedRestaurant.objects.filter(user=request.user, restaurant=restaurant).delete()
            bookmarked = False
        else:
            BookmarkedRestaurant.objects.create(user=request.user, restaurant=restaurant)
            bookmarked = True
        return JsonResponse({'success': True, 'bookmarked': bookmarked})