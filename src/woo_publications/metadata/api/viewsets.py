from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from ..models import InformationCategory, Theme
from .filters import InformationCategoryFilterSet
from .serializer import InformationCategorySerializer, ThemeSerializer


@extend_schema(tags=["Informatiecategorieën"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available information categories."),
        description=_(
            "Returns a paginated result list of existing information categories."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific information category."),
        description=_("Retrieve a specific information category."),
    ),
)
class InformationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterSet
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)


def _normalize_tree_dump(
    dump,
) -> models.QuerySet[Theme]:  # just to satisfy the viewset types
    # TODO: properly mimic the dump_bulk implementation but make it return (prefetched)
    result = []
    for node in dump:
        data = node["data"]
        data["sub_themes"] = _normalize_tree_dump(node.get("children", []))
        result.append(data)
    return result  # type: ignore


@extend_schema(tags=["Themas"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available themes."),
        description=_("Returns a paginated result list of existing themes."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific theme."),
        description=_("Retrieve a specific theme."),
    ),
)
class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all().order_by("pk")
    serializer_class = ThemeSerializer
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, node=None):  # type: ignore
        dumped = Theme.dump_bulk(node)
        return list(_normalize_tree_dump(dumped))

    # overwrite get_object func because the filtering that is caused by the retrieve endpoint breaks because of our fake queryset.
    def get_object(self):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            node = Theme.objects.get(**filter_kwargs)
            queryset = self.get_queryset(node)[0]
        # Extent the get_object_or_404 except errors with model.DoesNotExist and IndexError
        except (Theme.DoesNotExist, TypeError, ValueError, ValidationError, IndexError):
            raise Http404

        if not queryset:
            raise Http404

        self.check_object_permissions(self.request, queryset)

        return queryset
