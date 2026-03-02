from api.views.common_views import (
    OnlyByFilterMixin, BaseGenericViewSet)
from api.views.ies.serializers import (
    PeriodSimpleSerializer, InstitutionSerializer, InstitutionDetailSerializer)
from ies.models import Period, Institution


class PeriodViewSet(BaseGenericViewSet):

    queryset = Period.objects.all()
    serializer_class = PeriodSimpleSerializer


class InstitutionCatalogViewSet(BaseGenericViewSet):
    from django.db.models import Count
    queryset = Institution.objects.all()\
        .annotate(
        good_practice_packages_count=Count('packages'),
        good_practices_count=Count('packages__good_practices')
    )\
        .distinct()

    serializer_class = InstitutionSerializer

    def get_serializer_class(self):
        action_serializer = {
            'retrieve': InstitutionDetailSerializer,
            'update': InstitutionDetailSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)
