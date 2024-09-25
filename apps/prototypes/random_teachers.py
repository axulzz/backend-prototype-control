import random
from datetime import datetime as Date
from typing import List, Optional

from rest_framework.exceptions import ValidationError

from .models import Teacher, ModalityAssignment, TeacherRoles

randomize_teacher = lambda teachers: random.choice(teachers)

current_year = Date.now().year
start_date = Date(current_year, 1, 1).date()
end_date = Date(current_year, 12, 31).date()


"""
Esta funcion retorna los dos maestros asesores tecnico y metodologico
"""

def get_teachers_by_modality(modality: str) -> List[Optional[Teacher]]:
    try:
        modality_assignment = ModalityAssignment.objects.get(modality=modality)
    except ModalityAssignment.DoesNotExist:
        raise ValidationError({"error": f"No hay asignación de modalidad para '{modality}'"})

    academic_levels = modality_assignment.academic_level.all()

    if len(academic_levels) == 0:
        raise ValidationError({"error": f"No hay niveles académicos asociados a la modalidad '{modality}'"})

    data_t = Teacher.objects.filter(academic_level__in=academic_levels)
    data_m = Teacher.objects.all()

    pivot = 0
    while pivot <= 10:
        if not data_m or not data_t:
            raise ValidationError({"error": "No hay maestros disponibles"})

        teacher_t = randomize_teacher(data_t)
        teacher_m = randomize_teacher(data_m)

        queryset_rol_t = TeacherRoles.objects.filter(
            roles="AT",
            teacher_data=teacher_t,
            created__range=(start_date, end_date),
        )

        queryset_rol_m = TeacherRoles.objects.filter(
            roles="AM",
            teacher_data=teacher_m,
            created__range=(start_date, end_date),
        )

        if len(queryset_rol_t) >= 3:
            continue

        if len(queryset_rol_m) >= 3:
            continue
        
        pivot += 1

        return [teacher_m, teacher_t]

        

    raise ValidationError({"error": "No hay maestros disponibles para esta modalidad"})
