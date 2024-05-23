from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Restaurant, Employee, Menu, Vote


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_employee', 'is_restaurant')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Restaurant)
admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Vote)
