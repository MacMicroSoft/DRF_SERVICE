import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from faker import Faker
from rest_api.models import User, Restaurant, Menu, Employee, Vote
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

fake = Faker()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def get_tokens_for_user():
    def make_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    return make_tokens


@pytest.fixture
def restaurant_user(db, create_user):
    user = create_user(
        username=fake.user_name(),
        password='password',
        email=fake.email(),
        is_restaurant=True
    )
    Restaurant.objects.create(user=user, name=fake.company())
    return user


@pytest.fixture
def employee_user(db, create_user):
    user = create_user(
        username=fake.user_name(),
        password='password',
        email=fake.email(),
        is_employee=True
    )
    Employee.objects.create(user=user, name=fake.name())
    return user


@pytest.fixture
def menu(db, restaurant_user):
    return Menu.objects.create(
        restaurant=Restaurant.objects.get(user=restaurant_user),
        day_of_week=fake.day_of_week(),
        items=fake.json()
    )


@pytest.fixture
def authenticated_client(api_client, get_tokens_for_user):
    def make_authenticated_client(user):
        tokens = get_tokens_for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])
        return api_client

    return make_authenticated_client


@pytest.mark.django_db
def test_restaurant_create_menu(authenticated_client, restaurant_user):
    client = authenticated_client(restaurant_user)
    url = reverse('get_restaurant_week_menu')
    data = {
        'day_of_week': 'Monday',
        'items': fake.json()
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert Menu.objects.filter(restaurant__user=restaurant_user, day_of_week='Monday').exists()


@pytest.mark.django_db
def test_employee_vote_menu(authenticated_client, employee_user, menu):
    client = authenticated_client(employee_user)
    url = reverse('vote_menu', args=[menu.id])
    data = {
        'rating': True
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert Vote.objects.filter(employee__user=employee_user, menu=menu, rating=True).exists()


@pytest.mark.django_db
def test_employee_vote_twice(authenticated_client, employee_user, menu):
    client = authenticated_client(employee_user)
    url = reverse('vote_menu', args=[menu.id])
    data = {
        'rating': True
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.filter(employee__user=employee_user, menu=menu).count() == 1


@pytest.mark.django_db
def test_get_restaurant_week_menu(authenticated_client, restaurant_user, menu):
    client = authenticated_client(restaurant_user)
    url = reverse('get_restaurant_week_menu')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) > 0


@pytest.mark.django_db
def test_get_current_day_menu(authenticated_client, restaurant_user, menu):
    client = authenticated_client(restaurant_user)
    url = reverse('get-current-day-menu')
    current_day = date.today().strftime('%A')
    Menu.objects.create(
        restaurant=menu.restaurant,
        day_of_week=current_day,
        items=fake.json()
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.data


@pytest.mark.django_db
def test_get_menu_of_day(authenticated_client, restaurant_user, menu):
    client = authenticated_client(restaurant_user)
    url = reverse('current-day-votes')
    current_day = date.today().strftime('%A')
    Menu.objects.create(
        restaurant=menu.restaurant,
        day_of_week=current_day,
        items=fake.json()
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.data


@pytest.mark.django_db
def test_invalid_menu_creation(authenticated_client, restaurant_user):
    client = authenticated_client(restaurant_user)
    url = reverse('get_restaurant_week_menu')
    data = {
        'day_of_week': 'InvalidDay',
        'items': fake.json()
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data


@pytest.mark.django_db
def test_vote_for_nonexistent_menu(authenticated_client, employee_user):
    client = authenticated_client(employee_user)
    url = reverse('vote_menu', args=[999])
    data = {
        'rating': True
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.data
