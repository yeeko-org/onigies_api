from indicator.models import  Axis, Component, Observable, Sector
from api.views.common_views import BaseGenericViewSet
from api.views.indicator.serializers import (
    AxisSerializer, ComponentSerializer, ComponentFullSerializer,
    ObservableSerializer, SectorSerializer
)

class AxisViewSet(BaseGenericViewSet):
    queryset = Axis.objects.all()
    serializer_class = AxisSerializer


class ComponentViewSet(BaseGenericViewSet):
    queryset = Component.objects.all()
    filterset_fields = ['axis']
    serializer_class = ComponentFullSerializer

    def get_serializer_class(self):
        action_serializer = {
            'list': ComponentSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class ObservableViewSet(BaseGenericViewSet):
    queryset = Observable.objects.all()
    serializer_class = ObservableSerializer
    filterset_fields = ['component']


class SectorViewSet(BaseGenericViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

