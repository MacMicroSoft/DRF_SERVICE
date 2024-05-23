from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create/restaurant/', views.CreateRestaurantView.as_view(), name='create-restaurant'),
    path('create/employees/', views.CreateEmployeeView.as_view(), name='create-employee'),
    path('restaurant/menu/', views.RestaurantWeekMenuView.as_view(), name='get_restaurant_week_menu'),
    path('menus/today/', views.CurrentDayMenuView.as_view(), name='get-current-day-menu'),
    path('menus/vote/<int:menu_id>/', views.VoteMenuView.as_view(), name='vote_menu'),
    path('menus/current-day-votes/', views.MenuOfDayView.as_view(), name='current-day-votes'),
]

