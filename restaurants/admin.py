from django.contrib import admin
from .models import Restaurant, Photo, Dish, Review

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'location')
    search_fields = ('title', 'location')
    filter_horizontal = ('cuisines',)  # Ensure this matches the ManyToManyField in the model

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'description')
    search_fields = ('description',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'dish_type')
    search_fields = ('name', 'restaurant__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'visited', 'bookmarked')
    search_fields = ('user__username', 'restaurant__title')
