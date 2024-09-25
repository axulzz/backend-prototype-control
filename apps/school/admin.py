from django.contrib import admin

from apps.school.models import Student, Teacher

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "group",
        "specialty",
        "school_control_number",
    ]

    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "budget_code",
        "academic_level",
    ]

    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
