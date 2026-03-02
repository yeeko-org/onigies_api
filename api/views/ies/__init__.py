from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from api.views.common_views import BaseGenericViewSet
from api.views.ies.serializers import (
    InstitutionSimpleSerializer, InstitutionDetailSerializer)
from ies.models import Period, Institution


class InstitutionViewSet(BaseGenericViewSet):

    queryset = Institution.objects.all()
    serializer_class = InstitutionSimpleSerializer

    def partial_update(self, request, *args, **kwargs):
        # print("InstitutionViewSet.patch, request.data: ", request.data)
        super().partial_update(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'],
            parser_classes=[MultiPartParser, FormParser])
    def upload_logo(self, request, pk=None):
        institution = self.get_object()
        logo_file = request.FILES.get('logo')
        if logo_file:
            institution.logo.save(logo_file.name, logo_file)
            institution.save()
            return self.retrieve(request, pk=pk)
        else:
            return Response(
                {"detail": "No se ha proporcionado un archivo de logo."},
                status=status.HTTP_400_BAD_REQUEST)
