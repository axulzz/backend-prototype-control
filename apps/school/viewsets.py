from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.cores.models import GroupStudent
from apps.cores.serializers import (
    StudentCreateSerializer,
    StudentListSerializer,
    StudentRetrieveSerializer,
    TeacherCreateSerializer,
    TeacherListSerializer,
    TeacherRetrieveSerializer,
)
from apps.school.models import Student, Teacher
from apps.users.serializers import UserCreateSerializer, UserUpdateSerializer
from config.filters import StudentsFilters, TeachersFilters

User = get_user_model()


class StudentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    search_fields = ["user__email", "user__turn"]
    ordering_fields = ["group"]
    filterset_class = StudentsFilters

    def get_queryset(self):
        return Student.objects.all()

    def get_serializer_class(self):
        print(self.action)
        if self.action in ["create", "partial_update", "update"]:
            return StudentCreateSerializer

        if self.action in ["retrieve"]:
            return StudentRetrieveSerializer

        return StudentListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            group = GroupStudent.objects.get(id=data.get("group", None)).id
        except GroupStudent.DoesNotExist:
            group = None

        data.update({"group": group})

        serializer_user = UserCreateSerializer(
            data={
                "first_name": data.get("user").get("first_name", None),
                "last_name": data.get("user").get("last_name", None),
                "curp": data.get("user").get("curp", None),
                "email": data.get("user").get("email", None),
                "number_phone": data.get("user").get("number_phone", None),
                "address": data.get("user").get("address", None),
                "groups": [Group.objects.get(name="Alumno").pk],
                "turn": data.get("user").get("turn", None),
            }
        )
        serializer_user.is_valid(raise_exception=True)
        self.perform_create(serializer_user)

        data.update(
            {
                "user": serializer_user.data.get("id", None),  # type: ignore
            }
        )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if data.get("user", None) != None:

            serializer_user = UserUpdateSerializer(
                instance=User.objects.get(id=instance.user_id),
                data=data.get("user"),
                partial=partial,
            )
            serializer_user.is_valid(raise_exception=True)
            self.perform_update(serializer_user)

            data.update({"user": serializer_user.data.get("id", None)})  # type: ignore

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TeacherViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    search_fields = ["user__email", "user__first_name", "user__last_name", "user__curp"]
    ordering_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "budget_code, user__turn",
    ]

    filterset_class = TeachersFilters

    def get_queryset(self):
        return Teacher.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeacherCreateSerializer

        if self.action in ["retrieve"]:
            return TeacherRetrieveSerializer

        return TeacherListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        if not data.get("user", None):
            raise ValidationError({"user": "Este campo es requerido"})

        serializer_user = UserCreateSerializer(
            data={
                "first_name": data.get("user").get("first_name", None),
                "last_name": data.get("user").get("last_name", None),
                "curp": data.get("user").get("curp", None),
                "email": data.get("user").get("email", None),
                "number_phone": data.get("user").get("number_phone", None),
                "address": data.get("user").get("address", None),
                "groups": [Group.objects.get(name="Docente").pk],
                "turn": data.get("user").get("turn", None),
            }
        )
        serializer_user.is_valid(raise_exception=True)
        self.perform_create(serializer_user)

        data.update({"user": serializer_user.data.get("id", None)})  # type: ignore

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if data.get("user", None) != None:

            serializer_user = UserUpdateSerializer(
                instance=User.objects.get(id=instance.user_id),
                data=data.get("user"),
                partial=partial,
            )
            serializer_user.is_valid(raise_exception=True)
            self.perform_update(serializer_user)

            data.update({"user": serializer_user.data.get("id", None)})  # type: ignore

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
