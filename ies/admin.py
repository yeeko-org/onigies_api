from django.contrib import admin
from .models import Institution, StatusControl
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


@admin.register(StatusControl)
class StatusControlAdmin(admin.ModelAdmin):
    list_display = [
        "public_name", "name", "group", "order",
        "color", "icon", "priority"]
    list_editable = ["order", "color", "icon", "priority"]
    list_filter = ["group"]
