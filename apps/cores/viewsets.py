from rest_framework.viewsets import mixins, GenericViewSet

from apps.cores.models import AcademicLevel, GroupStudent, TypeInvestigation
from apps.cores.serializers import AcademyLevelSerializer, GroupStudentSerializer, TypeInvestigationSerializer


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


class GroupStudentsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer

    def get_queryset(self):
        return self.queryset
