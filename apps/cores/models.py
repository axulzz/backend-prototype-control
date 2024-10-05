from uuid import uuid4 as uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class BaselModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)

    class Meta:
        abstract = True


class CoreBase(BaselModel):
    """
    ## Model
    - text : str
    """

    text = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        abstract = True


class AcademicLevel(CoreBase):
    pass


class AcademicGroup(CoreBase):
    pass


class TypeInvestigation(CoreBase):
    pass
