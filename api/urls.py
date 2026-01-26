from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import health_check
from api.views.auth.login_views import UserLoginAPIView, CheckingViewSet

from api.views.ps_schemas.views import CollectionViewSet
from api.views.example.example_views import (
    GoodPracticeViewSet, GoodPracticePackageViewSet,
    FeatureGoodPracticeViewSet, EvidenceViewSet)
# from api.views.stop import StationViewSet
# from api.views.report import StairReportViewSet, AscertainableViewSet


router = DefaultRouter()

# router.register(r'station', StationViewSet, basename='station')
# router.register(r'stair_report', StairReportViewSet, basename='stair_report')
# router.register(
#     r'^stair_report/(?P<stair_report_id>[-\d]+)/evidence_image',
#     AscertainableViewSet,
#     basename='stair_report_evidence_image'
# )
# )
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'good_practice', GoodPracticeViewSet, basename='good_practice')
router.register(r'evidence', EvidenceViewSet, basename='evidence')
router.register(r'feature_good_practice', FeatureGoodPracticeViewSet, basename='feature_good_practice')
router.register(r'good_practice_package', GoodPracticePackageViewSet, basename='good_practice_package')
router.register(r'validate_token', CheckingViewSet, basename='validate_token')


urlpatterns = [
    # path('login/', obtain_auth_token, name='api-login'),
    path('health/', health_check, name='health_check'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('catalogs/', include('api.views.catalogs.urls')),
    # path('space_time/', include('api.views.space_time.urls')),
    path('', include(router.urls)),
]
