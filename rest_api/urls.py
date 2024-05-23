from django.contrib import admin
from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'weekly/menu/', views.CreateWeekMenuView)
# router.register(r'v1/empployee/', views.CreateEmployeeView)


urlpatterns = [
    path('auth/', views.RegisterView.as_view(), name='auth'),
    path('create/v1/restaurant/', views.CreateRestaurantView.as_view(), name='create_restaurant'),
    path('create/v1/employee/', views.CreateEmployeeView.as_view(), name='create_employee'),
    path('current/day/v1/menu/', views.GetCurrentDayMenuView.as_view(), name='current_day_menu'),
    path('rest/week/menu/', views.RestaurantWeekMenuView.as_view(), name='restaurant_week_menu')
    # path('', include(router.urls)),
]

