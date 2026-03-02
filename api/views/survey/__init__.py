from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.views.common_views import BaseGenericViewSet
from survey.models import Survey
from api.views.survey.serializers import SurveySerializer


class SurveyViewSet(BaseGenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

