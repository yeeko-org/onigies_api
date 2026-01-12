from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

# from ies.models import User
# from api.views.auth.serializers import UserProfileSerializer

from ies.models import Institution, Period, StatusControl
from indicator.models import Axis, Component, Observable, Sector
from example.models import Feature
from question.models import AOption
from ps_schema.models import Level, Collection, FilterGroup
from api.views.catalogs.serializers import (
    StatusControlSerializer,
    LevelSerializer,
    CollectionSerializer,
    FilterGroupSerializer,
    InstitutionSerializer,
    PeriodSerializer,
)
from api.views.indicator.serializers import (
    AxisSerializer,
    ComponentSerializer,
    ObservableSerializer,
    SectorSerializer,
)
from api.views.example.serializers import FeatureSerializer
from api.views.question.serializers import AOptionSerializer

class CatalogsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        catalogs = {
            # "user": UserProfileSerializer(
            #     User.objects.all(), many=True).data,
            "period": PeriodSerializer(
                Period.objects.all(), many=True).data,
            "institution": [],

            "status_control": StatusControlSerializer(
                StatusControl.objects.all(), many=True).data,
            "levels": LevelSerializer(
                Level.objects.all(), many=True).data,
            "collections": CollectionSerializer(
                Collection.objects.all(), many=True).data,
            "filter_groups": FilterGroupSerializer(
                FilterGroup.objects.all(), many=True).data,

            "axis": AxisSerializer(
                Axis.objects.all(), many=True).data,
            "component": ComponentSerializer(
                Component.objects.all(), many=True).data,
            "observable": ObservableSerializer(
                Observable.objects.all(), many=True).data,
            "sector": SectorSerializer(
                Sector.objects.all(), many=True).data,

            "feature": FeatureSerializer(
                Feature.objects.all(), many=True).data,
            "a_option": AOptionSerializer(
                AOption.objects.all(), many=True).data,
        }
        if self.request.user.is_authenticated:
            catalogs["institution"] = InstitutionSerializer(
                Institution.objects.all(), many=True).data,

        return Response(catalogs)
