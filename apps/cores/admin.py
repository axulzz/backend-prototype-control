from django.contrib import admin

from apps.cores.models import AcademicLevel, AcademicGroup, TypeInvestigation

# Register your models here.


@admin.register(AcademicGroup)
class AcademicGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]


@admin.register(TypeInvestigation)
class TypeInvestigationAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]


@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]
