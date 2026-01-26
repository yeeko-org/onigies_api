from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from example.models import (
    GoodPractice, Feature, FeatureOption, GoodPracticePackage,
    FeatureGoodPractice, Evidence)
from api.views.common_views import BaseGenericViewSet
from api.views.action_file import ActionFileMixin
from api.views.example.serializers import (
    GoodPracticeSerializer, FeatureSerializer, FeatureFullSerializer,
    FeatureOptionSerializer, FeatureGoodPracticeSerializer,
    GoodPracticePackageSerializer, GoodPracticePackageFullSerializer,
    GoodPracticeFullSerializer, EvidenceSerializer)



class GoodPracticeViewSet(BaseGenericViewSet, ActionFileMixin):

    queryset = GoodPractice.objects.all()
    serializer_class = GoodPracticeFullSerializer
    action_add_file_param = 'good_practice'
    disable_protection = True

    def get_serializer_class(self):
        action_serializer = {
            'list': GoodPracticeSerializer,
            'add_file': EvidenceSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class FeatureViewSet(BaseGenericViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_serializer_class(self):
        # print("FeatureViewSet.get_serializer_class, action: ", self.action)
        action_serializer = {
            'retrieve': FeatureFullSerializer,
            'create': FeatureFullSerializer,
            'update': FeatureFullSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class FeatureOptionViewSet(BaseGenericViewSet):
    queryset = FeatureOption.objects.all()
    serializer_class = FeatureOptionSerializer


class FeatureGoodPracticeViewSet(BaseGenericViewSet, ActionFileMixin):
    queryset = FeatureGoodPractice.objects.all()
    serializer_class = FeatureGoodPracticeSerializer
    action_add_file_param = 'feature_good_practice'

    def get_serializer_class(self):
        action_serializer = {
            'add_file': EvidenceSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class GoodPracticePackageViewSet(BaseGenericViewSet):
    queryset = GoodPracticePackage.objects.all()\
        .prefetch_related('good_practices')
    serializer_class = GoodPracticePackageFullSerializer
    search_fields = [
        'period__year', 'institution__name', 'institution__acronym']
    ordering_fields = ['id', 'period__year', 'institution__name']

    # pagination_class = CustomPagination
    # filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    def get_serializer_class(self):
        action_serializer = {
            'list': GoodPracticePackageSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        from django.utils import timezone
        good_practice_package = self.get_object()
        has_sent = good_practice_package.sent_at is not None
        status_register = "created" if not has_sent else "need_new_checking"
        good_practice_package.status_register_id = status_register
        if not has_sent:
            good_practice_package.sent_at = timezone.now()
        good_practice_package.save()
        pending_good_practices = good_practice_package.good_practices\
            .filter(status_register__is_final=False)
        for good_practice in pending_good_practices:
            good_practice.status_register_id = status_register
            good_practice.save()
        serializer = self.get_serializer(good_practice_package)
        return Response(serializer.data)


class EvidenceViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
