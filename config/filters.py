from django_filters import rest_framework as filters

from apps.cores.models import AcademicGroup
from apps.prototypes.models import Prototype
from apps.school.models import Student, Teacher


class UUIDInFilter(filters.BaseInFilter, filters.UUIDFilter):
    pass


class ChoiceInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class NumberInFilter(filters.NumberFilter):
    pass


class PrototypeFilters(filters.FilterSet):
    teacher_methods__in = UUIDInFilter(
        label="teacher_advisors__in", field_name="teacher_advisors", lookup_expr="in"
    )

    modality__in = ChoiceInFilter(
        label="modality__in", field_name="modality", lookup_expr="in"
    )

    created__gte = filters.DateFilter(
        label="created_(start)", field_name="created", lookup_expr="gte"
    )

    created__lte = filters.DateFilter(
        label="created_(end)", field_name="created", lookup_expr="lte"
    )

    qualification__gte = NumberInFilter(
        label="qualification__(start)", field_name="qualification", lookup_expr="gte"
    )

    qualification__lte = NumberInFilter(
        label="qualification__(end)", field_name="qualification", lookup_expr="lte"
    )

    class Meta:
        model = Prototype
        fields = [
            "name",
            "registry_number",
            "modality",
            "type_investigation",
            "qualification",
            "members",
            "teacher_methods",
            "teacher_advisors",
        ]


class PrototypeDonwloadFilters(filters.FilterSet):
    created__gte = filters.DateFilter(
        label="created_(start)", field_name="created", lookup_expr="gte"
    )

    created__lte = filters.DateFilter(
        label="created_(end)", field_name="created", lookup_expr="lte"
    )

    class Meta:
        model = Prototype
        fields = ["created"]


class TeachersFilters(filters.FilterSet):

    class Meta:
        model = Teacher
        fields = ["user", "budget_code", "academic_level", "created"]


class StudentsFilters(filters.FilterSet):
    class Meta:
        model = Student
        fields = [
            "user",
            "group",
            "specialty",
            "user__turn",
            "school_control_number",
            "created",
        ]


class GroupFilters(filters.FilterSet):
    class Meta:
        model = AcademicGroup
        fields = ["text"]
