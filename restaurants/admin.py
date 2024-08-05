from django.contrib import admin
from .models import Cuisine, Restaurant, Dish, Review

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'cost_for_two', 'owner', 'location', 'food_type', 'spotlight')
    list_filter = ('food_type', 'spotlight', 'owner')
    search_fields = ('title', 'location', 'address')
    readonly_fields = ('rating',)
    raw_id_fields = ('owner',)
    filter_horizontal = ('cuisines',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'dish_type')
    list_filter = ('dish_type', 'restaurant')
    search_fields = ('name', 'restaurant__title')
    raw_id_fields = ('restaurant',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'visited', 'bookmarked')
    list_filter = ('rating', 'visited', 'bookmarked', 'restaurant')
    search_fields = ('comment', 'user__username', 'restaurant__title')
    raw_id_fields = ('user', 'restaurant')