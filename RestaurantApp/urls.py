"""
URL configuration for RestaurantApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restaurants.views import RestaurantListView, RestaurantDetailView, DishListView, SpotlightRestaurantsView, VisitedRestaurantView, BookmarkedRestaurantView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('spotlight/', SpotlightRestaurantsView.as_view(), name = 'spotlight_restaurants'),
    path('visited/',VisitedRestaurantView.as_view(), name='visited_restaurants'),
    path('bookmarked/',BookmarkedRestaurantView.as_view(), name='bookmarked_restaurants'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurant/<int:pk>/dishes/', DishListView.as_view(), name='dish-list'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)