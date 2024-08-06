from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Restaurant, Cuisine
from .filters import RestaurantFilter

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
        context['sort_options'] = [
            ('cost_asc', 'Cost Low to High'),
            ('cost_desc', 'Cost High to Low'),
            ('rating_asc', 'Rating Low to High'),
            ('rating_desc', 'Rating High to Low')
        ]
        return context

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'