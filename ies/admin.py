from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ies.models import (
    Institution, StatusControl, User, PasswordRecoveryToken,
)
from survey.models import Survey
from example.models import GoodPracticePackage


# class PeriodInline(admin.TabularInline):
#     model = Period
#     extra = 0


class SurveyInline(admin.StackedInline):
    model = Survey
    extra = 0


class GoodPracticePackageInline(admin.StackedInline):
    model = GoodPracticePackage
    extra = 0


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym')
    search_fields = ('name', 'acronym')
    inlines = [SurveyInline, GoodPracticePackageInline]


@admin.register(PasswordRecoveryToken)
class PasswordRecoveryTokenAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'created_at', 'expires_at',
        'used_at', 'is_valid_display',
    ]
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = [
        'key', 'user', 'created_at', 'expires_at', 'used_at',
    ]

    @admin.display(boolean=True, description='¿Válido?')
    def is_valid_display(self, obj):
        return obj.is_valid()


@admin.register(StatusControl)
class StatusControlAdmin(admin.ModelAdmin):
    list_display = [
        "public_name", "name", "group", "order",
        "color", "icon", "priority"]
    list_editable = ["order", "color", "icon", "priority"]
    list_filter = ["group"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'reviewer')}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'institution')}),
        ('Información personal', {'fields': (
            'first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'reviewer', 'is_active'),
        }),
        ('Groups', {'fields': ('groups',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # ) + UserAdmin.fieldsets
    list_display = (
        'email', 'first_name', 'last_name',
        'is_active', 'reviewer', 'is_staff', 'institution')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-is_active', 'email')
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups', 'reviewer')

