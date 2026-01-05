from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from api.pagination import CustomPagination
from api.views.confirm_delete import CustomDeleteMixin


class AdvancedConditionalFieldsViewMixin(viewsets.ModelViewSet):
    """
    Advanced mixin that supports multiple permission levels
    """

    field_permissions = {
        'anonymous': [
            'status_register', 'comments', 'status_validation',
            'status_location'],
        'authenticated': [],  # Fields to exclude for authenticated users
        'staff': [],  # Fields to exclude for staff users
    }

    def get_excluded_fields(self):
        """
        Determine which fields to exclude based on user permissions
        """
        if self.request.user.is_staff:
            return self.field_permissions.get('staff', [])
        elif self.request.user.is_authenticated:
            return self.field_permissions.get('authenticated', [])
        else:
            return self.field_permissions.get('anonymous', [])

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        excluded_fields = self.get_excluded_fields()
        # print("get_serializer, excluded_fields: ", excluded_fields)
        if excluded_fields:
            kwargs['exclude_fields'] = excluded_fields

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UnaccentSearchFilter(SearchFilter):

    def construct_search(self, field_name, queryset):
        from django.db.models.constants import LOOKUP_SEP
        if not field_name:
            return None
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
            return LOOKUP_SEP.join([field_name, lookup])
        else:
            return LOOKUP_SEP.join([field_name, 'unaccent', 'icontains'])


class BaseViewSet(CustomDeleteMixin, viewsets.ModelViewSet):

    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class OrderingAutoFilter(OrderingFilter):

    def get_valid_fields(self, queryset, view, context={}):
        from ies.models import StatusControl
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)

        if valid_fields is None:
            return super().get_valid_fields(queryset, view, context)

        final_valid_fields = super().get_valid_fields(queryset, view, context)

        if '__auto__' in valid_fields:
            all_fields = queryset.model._meta.fields
            for field in all_fields:
                if field.many_to_one:
                    if issubclass(field.related_model, StatusControl):
                        field_str = f'{field.name}__order'
                        final_valid_fields.append((field_str, field_str))
                elif field.primary_key:
                    final_valid_fields.append((field.name, field.name))
                elif field.name in ['name', 'title', 'order']:
                    final_valid_fields.append((field.name, field.name))
        return final_valid_fields


class BaseGenericViewSet(BaseViewSet):
    filterset_fields = []
    ordering_fields = ['__auto__']
    filter_backends = [
        UnaccentSearchFilter, DjangoFilterBackend, OrderingAutoFilter]


class BaseStatusViewSet(BaseGenericViewSet):
    filterset_fields = ['status_validation']


class MassiveEdit(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'])
    def massive_edit(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        elements_ids = request.data.pop('elems_ids')

        update_data = {}
        # for field in self.massive_fields:
        for field in data:
            update_data[field] = data[field]

        queryset = self.get_queryset()
        elements = queryset.filter(id__in=elements_ids)
        elements.update(**update_data)

        list_serializer = self.get_serializer(elements, many=True)
        return Response(list_serializer.data)

    @action(detail=True, methods=['patch'])
    def massive_patch(self, request, pk=None):
        elements_ids = request.data.pop('elems_ids')
        print("elements_ids: ", elements_ids)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        update_data = {}
        # for field in self.massive_fields:
        for field in data:
            update_data[field] = data[field]

        queryset = self.get_queryset()
        elements = queryset.filter(id__in=elements_ids)
        elements.update(**update_data)

        list_serializer = self.get_serializer(elements, many=True)
        return Response(list_serializer.data)


class OnlyByFilterMixin(FilterSet):

    only_by = CharFilter(method='filter_only_by')
    only_options = ["project", "event", "impact"]

    def filter_only_by(self, queryset, name, value):
        if value not in self.only_options:
            return queryset

        filter_kwargs = {f"{value}__isnull": False}
        return queryset.filter(**filter_kwargs)


# class UnaccentMixin(viewsets.GenericViewSet):
#
#     search_fields = ['name']
#
#     def filter_queryset(self, queryset):
#         from django.db.models import Q
#         queryset = super().filter_queryset(queryset)
#         search_query = self.request.query_params.get('q', '')
#         print('filter_queryset, search_query: ', search_query)
#         print('search_fields: ', self.search_fields)
#         if search_query:
#             filter_query = Q()
#             for field in self.search_fields:
#                 filter_query |= Q(**{f'{field}__unaccent__icontains': search_query})
#                 # filter_query |= Q(**{f'{field}__icontains': search_query})
#                 print('filter_query: ', filter_query)
#             queryset = queryset.filter(filter_query)
#
#         return queryset
