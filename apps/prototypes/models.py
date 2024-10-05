from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.cores.models import AcademicLevel, BaselModel, TypeInvestigation
from apps.school.models import Student, Teacher

# Create your models here.


class ModalityChoices(models.TextChoices):
    TECNOLOGICO = "TEC", _("Tecnologico")
    SOFTWARE = "SW", _("Software")
    DIDACTICO = "DC", _("Didactico")
    EMPRENDEDOR_VERDE = "EV", _("Emprendedor Verde")
    EMPRENDEDOR_SOCIAL = "ES", _("Emprendedor Social")
    EMPRENDEDOR_TECNOLOGICO = "ET", _("Emprendedor Tecnologico")


class ModalityAssignment(BaselModel):
    academic_level = models.ManyToManyField(AcademicLevel)
    modality = models.CharField(
        max_length=6, blank=False, null=False, choices=ModalityChoices.choices
    )


class TeacherRoles(BaselModel):
    """
    ## Model
    - teacher_data : uuid,
    - roles : char, choices,
    """

    class Roles(models.TextChoices):
        Asesor_Metodologico = "AM", _("Asesor de metodologico")
        Asesor_Tecnico = "AT", _("Asesor tecnico")

    teacher_data = models.ForeignKey(Teacher, models.CASCADE, null=False)
    roles = models.CharField(
        choices=Roles.choices,
        max_length=30,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.teacher_data.user.email}"


class Member(BaselModel):
    """
    ## Model
    - student : uuid,
    - author : int,
    """

    student = models.OneToOneField(
        Student, models.CASCADE, null=False, blank=False, unique=True
    )
    author = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ("author",)

    def __str__(self) -> str:
        return f"{self.student.user.email}"  # type: ignore


class Prototype(BaselModel):
    """
    ## Model
    - name : string,
    - registry_number : string,
    - modality : char, choices,
    - type_investigation : uuid,
    - qualification : int,
    - members : uuid[],
    - teacher_methods : uuid,
    - teacher_advisors : uuid[],
    """

    name = models.CharField(max_length=256, null=False, blank=False)
    registry_number = models.CharField(
        max_length=10, unique=True, null=False, blank=False
    )
    modality = models.CharField(
        max_length=3,
        choices=ModalityChoices.choices,
        null=False,
        blank=False,
    )
    type_investigation = models.ForeignKey(
        TypeInvestigation, models.CASCADE, null=True, blank=False
    )
    qualification = models.IntegerField(null=True, blank=False, default=0)
    members = models.ManyToManyField(Member)
    teacher_methods = models.ForeignKey(Teacher, models.CASCADE, null=True, blank=False)
    teacher_advisors = models.ManyToManyField(TeacherRoles)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.name}"
