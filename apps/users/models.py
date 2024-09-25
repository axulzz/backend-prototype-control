import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):
    """
    ## Model
    - id : string
    - email : string
    - address : string
    - number_phone : integer
    - curp : string
    - turn : choices
    """

    class Turn(models.TextChoices):
        Vespertine = "T/V", _("Vespertino")
        Morning = "T/M", _("Matutino")

    turn = models.CharField(
        max_length=3,
        choices=Turn.choices,
        null=False,
        blank=False,
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_("email address"), unique=True)
    # email_personal = models.EmailField(_("personal name"), unique=True, null=True)

    address = models.TextField(null=True, blank=True)
    number_phone = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(default=None, null=False, blank=True)
    curp = models.CharField(
        null=False,
        blank=False,
        max_length=18,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        return self.email
