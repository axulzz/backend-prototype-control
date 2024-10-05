from rest_framework.viewsets import mixins, GenericViewSet

from apps.cores.models import AcademicLevel, AcademicGroup, TypeInvestigation
from apps.cores.serializers import (
    AcademyLevelSerializer,
    AcademicGroupSerializer,
    TypeInvestigationSerializer,
)


class AcademyLevelViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = AcademicLevel.objects.all()
    serializer_class = AcademyLevelSerializer

    def get_queryset(self):
        return self.queryset


class TypeInvestigationViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TypeInvestigation.objects.all()
    serializer_class = TypeInvestigationSerializer

    def get_queryset(self):
        return self.queryset


class AcademicGroupViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AcademicGroupSerializer

    def get_queryset(self):
        return AcademicGroup.objects.all()
