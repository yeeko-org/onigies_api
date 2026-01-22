from api.views.common_views import BaseGenericViewSet
from example.models import (
    GoodPractice, Feature, FeatureOption, GoodPracticePackage,
    FeatureGoodPractice, Evidence)
from api.views.action_file import ActionFileMixin
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.views.example.serializers import (
    GoodPracticeSerializer, FeatureSerializer, FeatureFullSerializer,
    FeatureOptionSerializer, FeatureGoodPracticeSerializer,
    GoodPracticePackageSerializer, GoodPracticeFullSerializer,
    EvidenceSerializer)



class GoodPracticeViewSet(BaseGenericViewSet, ActionFileMixin):

    queryset = GoodPractice.objects.all()
    serializer_class = GoodPracticeFullSerializer
    action_add_file_param = 'good_practice'

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
    queryset = GoodPracticePackage.objects.all()
    serializer_class = GoodPracticePackageSerializer


class NoteFileViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
