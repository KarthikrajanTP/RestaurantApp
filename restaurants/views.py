from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Restaurant, Cuisine, Review, Dish
from .filters import RestaurantFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ReviewForm
from django.core.paginator import Paginator

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs

        sort_option = self.request.GET.get('sort_by')
        if sort_option == 'cost_asc':
            queryset = queryset.order_by('cost_for_two')
        elif sort_option == 'cost_desc':
            queryset = queryset.order_by('-cost_for_two')
        elif sort_option == 'rating_asc':
            queryset = queryset.order_by('rating')
        elif sort_option == 'rating_desc':
            queryset = queryset.order_by('-rating')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['cuisines'] = Cuisine.objects.all()
        context['food_types'] = Restaurant.FOOD_TYPE_CHOICES
        context['ratings'] = [1, 2, 3, 4, 5]
        context['cost_ranges'] = [200, 500, 1000, 2000, 3000]
        context['sort_options'] = [
            ('cost_asc', 'Cost Low to High'),
            ('cost_desc', 'Cost High to Low'),
            ('rating_asc', 'Rating Low to High'),
            ('rating_desc', 'Rating High to Low')
        ]
        return context

class RestaurantDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        reviews = restaurant.reviews.all()

        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        user_review = reviews.filter(user=request.user).first()
        review_form = ReviewForm(instance=user_review)

        return render(request, 'restaurant_detail.html', {
            'restaurant': restaurant,
            'page_obj': page_obj,
            'review_form': review_form,
            'user_review': user_review
        })

    def post(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        user_review = restaurant.reviews.filter(user=request.user).first()

        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()

        return redirect('restaurant-detail', pk=pk)
    
class DishListView(ListView):
    model = Dish
    template_name = 'dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 9

    def get_queryset(self):
        restaurant_id = self.kwargs.get('pk')
        return Dish.objects.filter(restaurant_id=restaurant_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        context['restaurant'] = restaurant
        return context