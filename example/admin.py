from django.contrib import admin
from .models import (
    GoodPracticePackage, GoodPractice, FeatureGoodPractice, Feature)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


class FeatureGoodPracticeInline(admin.StackedInline):
    model = FeatureGoodPractice
    extra = 0


@admin.register(GoodPractice)
class GoodPracticeAdmin(admin.ModelAdmin):
    list_display = ('package', 'axis', 'name')
    list_filter = ('package__period__year',)
    inlines = [FeatureGoodPracticeInline]


class GoodPracticeInline(admin.StackedInline):
    model = GoodPractice
    show_change_link = True
    extra = 0


@admin.register(GoodPracticePackage)
class GoodPracticePackageAdmin(admin.ModelAdmin):
    list_display = ('period', 'institution')
    search_fields = ('institution__name', 'institution__acronym')
    list_filter = ('period__year',)
    inlines = [GoodPracticeInline]

