import openpyxl
from io import BytesIO

from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.renderers import XLSXRenderer
from drf_excel.mixins import XLSXFileMixin

from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from rest_framework.renderers import BaseRenderer
from openpyxl.utils import get_column_letter


class CustomXLSXRenderer(XLSXRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        response = renderer_context["response"]
        view = renderer_context["view"]

        wb = openpyxl.Workbook()
        ws = wb.active

        # Set the filename from the view
        filename = getattr(view, "filename", "export.xlsx")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        # Get column headers from the view
        column_header = getattr(view, "column_header", {})
        column_titles = column_header.get("titles", [])

        # Write column headers to the first row
        for col_num, title in enumerate(column_titles, 1):
            cell = ws.cell(row=1, column=col_num, value=title)
            cell.font = Font(bold=True)

        # Save the workbook to the response
        output = BytesIO()
        wb.save(output)
        return output.getvalue()

class TemplateBase(XLSXFileMixin, ReadOnlyModelViewSet):
    renderer_classes = (CustomXLSXRenderer,)

class TeacherTemplate(TemplateBase):
    filename = "PlantillaMaestros.xlsx"
    column_header = {
        "titles": [

        ]
    }

class StudentTamplete(TemplateBase):
    filename = "PlantillaAlumnos.xlsx"
    column_header = {
        "titles": [
            
        ]
    }

class CustomPrototypeXLSXRenderer(BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'

    MODALIDAD_CHOICES = [
        "Tecnologico",
        "Software",
        "Didactico",
        "Emprendedor Verde",
        "Emprendedor Social",
        "Emprendedor Tecnologico"
    ]

    LINEA_INVESTIGACION_CHOICES = [
        "Desarrollo Tecnológico",
        "Desarrollo humano",
        "Social y Emocional",
        "Desarrollo Sustentable y Medio Ambiente",
        "Investigación de Ciencias de la Salud",
        "Investigación Educativa"
    ]

    def render(self, data, media_type=None, renderer_context=None):
        response = renderer_context['response']
        view = renderer_context['view']

        wb = openpyxl.Workbook()
        ws = wb.active

        # Set the filename from the view
        filename = getattr(view, 'filename', 'export.xlsx')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Get column headers from the view
        column_header = getattr(view, 'column_header', {})
        column_titles = column_header.get('titles', [])

        # Write column headers to the first row
        for col_num, title in enumerate(column_titles, 1):
            cell = ws.cell(row=1, column=col_num, value=title)
            cell.font = Font(bold=True)

        # Define data validation for lists
        modalidad_choices = ','.join(self.MODALIDAD_CHOICES)
        modalidad_validation = DataValidation(
            type="list",
            formula1=f'"{modalidad_choices}"',
            allow_blank=True,
            showDropDown=True
        )
        
        linea_investigacion_choices = ','.join(self.LINEA_INVESTIGACION_CHOICES)
        print(linea_investigacion_choices)
        linea_investigacion_validation = DataValidation(
            type="list",
            formula1=f'"{linea_investigacion_choices}"',
            allow_blank=True,
            showDropDown=True
        )

        # Apply data validations to the appropriate columns
        modalidad_column = None
        linea_investigacion_column = None
        for col_num, title in enumerate(column_titles, 1):
            if title == "Modalidad":
                modalidad_column = col_num
            elif title == "Línea de Investigación":
                linea_investigacion_column = col_num

        if modalidad_column:
            modalidad_column_letter = get_column_letter(modalidad_column)
            modalidad_range = f'{modalidad_column_letter}2:{modalidad_column_letter}1048576'
            modalidad_validation.add(modalidad_range)
        
        if linea_investigacion_column:
            linea_investigacion_column_letter = get_column_letter(linea_investigacion_column)
            linea_range = f'{linea_investigacion_column_letter}2:{linea_investigacion_column_letter}1048576'
            linea_investigacion_validation.add(linea_range)

        # Add data validations to the worksheet
        ws.add_data_validation(modalidad_validation)
        ws.add_data_validation(linea_investigacion_validation)

        # Save the workbook to the response
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output.getvalue()

class PrototypeTemplate(TemplateBase):
    filename = "PlatillasPrototipos.xlsx"
    renderer_classes = (CustomPrototypeXLSXRenderer,)
    column_header = {
        "titles": [
            "Nombre del prototipo",
            "Modalidad",
            "Línea de Investigación",
            "Maestro de Métodos",
            "ASESOR METODOLOGICO",
            "ASESOR TECNICO",
            "Autor 1",
            "NOMBRE COMPLETO",
            "Autor 2",
            "NOMBRE COMPLETO",
            "Autor 3",
            "NOMBRE COMPLETO",
            "Autor 4",
            "NOMBRE COMPLETO",
        ],
    }

class PrototypeDonwload(TemplateBase):
    filename = "PlatillasPrototipos.xlsx"
    column_header = {
        "titles": [
            "NOMBRE PROTOTIPO",
            "NUMERO REGISTRO",
            "Modalidad ",
            "Línea de Investigación",
            "Cal. Preeselección",
            "Maestro de Métodos",
            "ASESOR METODOLOGICO",
            "CLAVE PRESUPUESTAL",
            "NIVEL ACADEMICO ",
            "EMAIL ASESOR",
            "DIRECCION",
            "TELÉFONO",
            "ASESOR TECNICO",
            "CLAVE PRESUPUESTA",
            "NIVEL ACADEMICO",
            "EMAIL ASESOR",
            "DIRECCIÓN",
            "TELÉFONO",
            "Autor",
            "NOMBRE COMPLETO",
            "GRUPO",
            "ESPECIALIDAD",
            "TURNO",
            "No. DE CONTROL ESCOLAR",
            "CORREO INSTITUCIONAL",
            "DIRECCION",
            "TELEFONO",
            "Autor",
            "NOMBRE COMPLETO",
            "GRUPO",
            "ESPECIALIDAD",
            "TURNO",
            "No. DE CONTROL ESCOLAR",
            "CORREO INSTITUCIONAL",
            "DIRECCION",
            "TELEFONO",
            "Autor",
            "NOMBRE COMPLETO",
            "GRUPO",
            "ESPECIALIDAD",
            "TURNO",
            "No. DE CONTROL ESCOLAR",
            "CORREO INSTITUCIONAL",
            "DIRECCION",
            "TELEFONO",
            "Autor",
            "NOMBRE COMPLETO",
            "GRUPO",
            "ESPECIALIDAD",
            "TURNO",
            "No. DE CONTROL ESCOLAR",
            "CORREO INSTITUCIONAL",
            "DIRECCION",
            "TELEFONO",
        ],
    }
