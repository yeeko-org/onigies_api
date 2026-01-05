from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.register_merge import related_objects_report


# class CustomDeleteMixin(viewsets.ModelViewSet):
class CustomDeleteMixin:

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # type: ignore

        report_data = []
        errors = []
        related_objects_report(
            instance, instance._meta.related_objects, report_data, errors)

        for report in report_data:
            if report["affected_records"]:
                return Response(
                    {"report_data": report_data, "errors": errors},
                    status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)  # type: ignore

    @action(detail=True, methods=["delete"], url_path="confirm-delete")
    def confirm_delete(self, request, pk=None):
        instance = self.get_object()  # type: ignore
        instance.delete()
        return Response({"detail": "All information deleted."}, status=status.HTTP_204_NO_CONTENT)
