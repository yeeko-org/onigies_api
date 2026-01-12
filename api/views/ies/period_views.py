from api.views.common_views import (
    OnlyByFilterMixin, BaseGenericViewSet)
from api.views.ies.serializers import (
    PeriodSimpleSerializer, InstitutionSimpleSerializer)
from ies.models import Period, Institution


class PeriodViewSet(BaseGenericViewSet):

    queryset = Period.objects.all()
    serializer_class = PeriodSimpleSerializer


class InstitutionViewSet(BaseGenericViewSet):

    queryset = Institution.objects.all()
    serializer_class = InstitutionSimpleSerializer
