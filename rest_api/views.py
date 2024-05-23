from datetime import date
import calendar
from django.shortcuts import render
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, viewsets
from .models import User, Restaurant, Menu, Vote, Employee
from .serializers import (
    MenuSerializer,
    RestaurantSerializer,
    CustomUserSerializer,
    VoteSerializer,
    RegisterSerializer,
    EmployeeSerializer
)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer


class CreateRestaurantView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        user = self.request.user
        user.is_restaurant = True
        user.save()
        serializer.save(user=user)


class CreateEmployeeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        user.is_employee = True
        user.save()
        serializer.save(user=user)


class RestaurantWeekMenuView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        menus = Menu.objects.filter(restaurant=request.user.restaurant)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=request.user.restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentDayMenuView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MenuSerializer

    def get(self, request):
        day_of_week = date.today().strftime('%A')
        try:
            menu = Menu.objects.get(day_of_week=day_of_week)
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({"detail": "Menu not found for today"}, status=status.HTTP_404_NOT_FOUND)


class VoteMenuView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    def post(self, request, menu_id, *args, **kwargs):
        employee = request.user.employee
        rating = request.data.get('rating', True)
        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({"detail": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        existing_vote = Vote.objects.filter(employee=employee, menu=menu)
        if existing_vote.exists():
            return Response({"detail": "You have already voted for this menu item."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = VoteSerializer(data={'employee': employee.pk, 'menu': menu_id, 'rating': rating})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuOfDayView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MenuSerializer

    def get_object(self):
        current_day = date.today().strftime('%A')
        try:
            menu_of_day = Menu.objects.filter(day_of_week=current_day)\
                .annotate(num_votes=Count('vote'))\
                .filter(num_votes__gt=0, vote__rating=True)\
                .order_by('-num_votes').first()
        except Menu.DoesNotExist:
            menu_of_day = None

        return menu_of_day

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
