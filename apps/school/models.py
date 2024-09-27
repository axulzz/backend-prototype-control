from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.cores.models import AcademicLevel, BaselModel, GroupStudent

User = get_user_model()

# Create your models here.


class Teacher(BaselModel):
    """
    ## Model
    - budget_code : string
    - academic_level : uuid
    - user : uuid
    """

    # class Turn(models.TextChoices):
    #     Vespertine = "T/V", _("Vespertino")
    #     Morning = "T/M", _("Matutino")

    budget_code = models.CharField(max_length=256, blank=False, null=False)
    academic_level = models.ForeignKey(
        AcademicLevel, models.CASCADE, null=False, blank=False
    )
    cedual_profecional = models.CharField(max_length=256, null=False, blank=False)
    user = models.ForeignKey(User, models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.user}"


class Student(BaselModel):
    """
    ## Model
    - Group : uuid,
    - Specialty : char, choices,
    - school_control_number : int,
    - user : uuid,
    """

    class Specialty(models.TextChoices):
        TECNICO_EN_PROGRAMACION = "TEP", _("TECNICO EN PROGRAMACION")
        TECNICO_EN_CONTABILIDAD = "TEC", _("TECNICO EN CONTABILIDAD")
        TECNICO_EN_SECRETARIADO_EJECUTIVO_BILINGUE = "TESEB", _(
            "TECNICO EN SECRETARIADO EJECUTIVO BILINGUE"
        )
        TECNICO_EN_CIENCIA_DE_DATOS_E_INFORMACION = "TECDEI", _(
            "TECNICO EN CIENCIA DE DATOS E INFORMACION"
        )

    # class Turn(models.TextChoices):
    #     Vespertine = "T/V", _("Vespertino")
    #     Morning = "T/M", _("Matutino")

    group = models.ForeignKey(GroupStudent, models.CASCADE, null=False, blank=False)
    specialty = models.CharField(
        max_length=6,
        choices=Specialty.choices,
        null=False,
        blank=False,
    )

    # turn = models.CharField(
    #     max_length=3,
    #     choices=Turn.choices,
    #     null=False,
    #     blank=False,
    # )
    school_control_number = models.CharField(null=False, blank=False, max_length=256)

    user = models.ForeignKey(User, models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f"Email: {self.user}"
