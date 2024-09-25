from django.contrib import admin

from apps.prototypes.models import Member, ModalityAssignment, Prototype, TeacherRoles

# Register your models here.


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "student"]


@admin.register(Prototype)
class PrototypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "registry_number", "modality", "created"]

@admin.register(ModalityAssignment)
class ModalityAssignmentAdmin(admin.ModelAdmin):
    list_display = ["id", "modality"]


@admin.register(TeacherRoles)
class TeacherRolesAdmin(admin.ModelAdmin):
    list_display = ["id", "teacher_data", "roles"]
