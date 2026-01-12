from django.urls import include, path
from rest_framework import routers

from api.views.catalogs.all import CatalogsView
from api.views.ies.period_views import PeriodViewSet, InstitutionViewSet
from api.views.example.example_views import (
    FeatureViewSet, FeatureOptionViewSet, FeatureGoodPracticeViewSet,
    GoodPracticePackageViewSet)
from api.views.indicator.indicator_views import (
    AxisViewSet, ComponentViewSet, ObservableViewSet, SectorViewSet)

router = routers.DefaultRouter()

# router.register(r'source', SourceViewSet, basename='catalog_source')
# router.register(r'status_control', StatusControlViewSet, basename='catalog_status_control')
router.register(r'period', PeriodViewSet, basename='period')
router.register(r'institution', InstitutionViewSet, basename='institution')
router.register(r'feature', FeatureViewSet, basename='feature')
router.register(r'feature_option', FeatureOptionViewSet, basename='feature_option')
router.register(r'feature_good_practice', FeatureGoodPracticeViewSet, basename='feature_good_practice')
router.register(r'good_practice_package', GoodPracticePackageViewSet, basename='good_practice_package')
router.register(r'axis', AxisViewSet, basename='axis')
router.register(r'component', ComponentViewSet, basename='component')
router.register(r'observable', ObservableViewSet, basename='observable')
router.register(r'sector', SectorViewSet, basename='sector')


urlpatterns = [
    path("all/", CatalogsView.as_view(), name="catalogs_all"),
    path('', include(router.urls)),
]