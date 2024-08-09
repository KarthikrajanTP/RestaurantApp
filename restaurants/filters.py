import django_filters
from .models import Cuisine, Restaurant

class RestaurantFilter(django_filters.FilterSet):
    cuisines = django_filters.ModelChoiceFilter(
        queryset=Cuisine.objects.all(),
        empty_label='All Cuisines',
        to_field_name='id', 
        label='Cuisine'
    )
    food_type = django_filters.ChoiceFilter(
        choices=Restaurant.FOOD_TYPE_CHOICES,
        empty_label='All Types',
        label='Food Type'
    )
    rating = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Minimum Rating'
    )
    cost = django_filters.NumberFilter(
        field_name='cost_for_two',
        lookup_expr='lte',
        label='Maximum Cost for Two'
    )
    city = django_filters.CharFilter(
        field_name='location',
        lookup_expr='icontains',
        label='Search by City'
    )
    o = django_filters.OrderingFilter(
        choices=[
            ('cost_for_two', 'Cost Low to High'),
            ('-cost_for_two', 'Cost High to Low'),
            ('rating', 'Rating Low to High'),
            ('-rating', 'Rating High to Low'),
        ],

    )

    class Meta:
        model = Restaurant
        fields = ['cuisines', 'food_type', 'rating', 'cost', 'city']
