from api.views.common_views import BaseGenericViewSet
from example.models import (
    GoodPractice, Feature, FeatureOption, GoodPracticePackage,
    FeatureGoodPractice)
from api.views.example.serializers import (
    GoodPracticeSerializer, FeatureSerializer, FeatureFullSerializer,
    FeatureOptionSerializer, FeatureGoodPracticeSerializer,
    GoodPracticePackageSerializer)


class GoodPracticeViewSet(BaseGenericViewSet):

    queryset = GoodPractice.objects.all()
    serializer_class = GoodPracticeSerializer


class FeatureViewSet(BaseGenericViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_serializer_class(self):
        print("FeatureViewSet.get_serializer_class, action: ", self.action)
        action_serializer = {
            'retrieve': FeatureFullSerializer,
            'create': FeatureFullSerializer,
            'update': FeatureFullSerializer,
        }
        return action_serializer.get(self.action, self.serializer_class)


class FeatureOptionViewSet(BaseGenericViewSet):
    queryset = FeatureOption.objects.all()
    serializer_class = FeatureOptionSerializer


class FeatureGoodPracticeViewSet(BaseGenericViewSet):
    queryset = FeatureGoodPractice.objects.all()
    serializer_class = FeatureGoodPracticeSerializer


class GoodPracticePackageViewSet(BaseGenericViewSet):
    queryset = GoodPracticePackage.objects.all()
    serializer_class = GoodPracticePackageSerializer

