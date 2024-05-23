from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import calendar
from rest_framework.permissions import IsAuthenticated
from .models import User, Restaurant, Menu, Vote, Employee
from rest_framework import generics, viewsets
from .serializers import MenuSerializer, RestaurantSerializer, CustomUserSerializer, VoteSerializer, RegisterSerializer,\
    EmployeeSerializer
from datetime import date


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


class GetCurrentDayMenuView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MenuSerializer

    def get(self, request):
        my_date = date.today()
        day_of_week = calendar.day_name[my_date.weekday()]
        try:
            menu = Menu.objects.get(day_of_week=day_of_week)
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({"detail": "Menu not found for today"}, status=status.HTTP_404_NOT_FOUND)


class VoteCurrentDayMenuView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = VoteSerializer

