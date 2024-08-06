from django.shortcuts import render
from django.views.generic import ListView
from .models import Restaurant, Cuisine

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        
        selected_cuisine = self.request.GET.get('cuisine')
        if selected_cuisine:
            try:
                selected_cuisine = int(selected_cuisine)
                queryset = queryset.filter(cuisines__id=selected_cuisine).distinct()
            except ValueError:
                pass

        food_type = self.request.GET.get('food_type')
        if food_type:
            queryset = queryset.filter(food_type=food_type)

        rating = self.request.GET.get('rating')
        if rating:
            try:
                rating = float(rating)
                queryset = queryset.filter(rating__gte=rating)
            except ValueError:
                pass

        cost = self.request.GET.get('cost')
        if cost:
            try:
                cost = float(cost)
                queryset = queryset.filter(cost_for_two__lte=cost)
            except ValueError:
                pass

        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by == 'cost_asc':
                queryset = queryset.order_by('cost_for_two')
            elif sort_by == 'cost_desc':
                queryset = queryset.order_by('-cost_for_two')
            elif sort_by == 'rating_asc':
                queryset = queryset.order_by('rating')
            elif sort_by == 'rating_desc':
                queryset = queryset.order_by('-rating')

        search_city = self.request.GET.get('city')
    
        if search_city:
            queryset = queryset.filter(location__icontains=search_city)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuisines'] = Cuisine.objects.all()
        context['food_types'] = Restaurant.FOOD_TYPE_CHOICES
        context['ratings'] = [1, 2, 3, 4, 5]
        context['cost_ranges'] = [10, 20, 30, 40, 50]
        context['sort_options'] = [
            ('cost_asc', 'Cost Low to High'),
            ('cost_desc', 'Cost High to Low'),
            ('rating_asc', 'Rating Low to High'),
            ('rating_desc', 'Rating High to Low')
        ]
        return context
