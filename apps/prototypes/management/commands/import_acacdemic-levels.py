from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

import openpyxl
from apps.cores.models import AcademicLevel

User = get_user_model()


class Command(BaseCommand):
    help = "Este comando crea maestros"

    def handle(self, *args, **options):
        excel_file_path = "teachers_import.xlsx"
        max_rows = 72
        error_count = 0

        try:
            # Abre el archivo Excel
            workbook = openpyxl.load_workbook(excel_file_path, read_only=True)

            # Obtiene la hoja activa
            sheet = workbook.active

            # Itera sobre las filas de la hoja
            for row_number, row in enumerate(sheet.iter_rows(values_only=True, max_row=max_rows)): # type: ignore #
                try:
                    if len(row) >= max_rows:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error en la fila {row_number}: Número incorrecto de valores. Verifica la estructura del archivo Excel."
                            )
                        )
                        error_count += 1
                        continue

                    if row_number >= 2:
                        AcademicLevel.objects.create(text=row[7])
                        # )

                        # self.stdout.write(self.style.SUCCESS(f"Creado maestro: {teacher}"))
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error al procesar la fila {row_number}: {str(e)}."
                        )
                    )
                    error_count += 1

            self.stdout.write(
                self.style.SUCCESS("Proceso completado exitosamente.")
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Error: No se encontró el archivo {excel_file_path}.")
            )
        except Exception as e:
            # self.stdout.write(
            #     self.style.ERROR(f"Error al procesar el archivo Excel: {str(e)}")
            # )
            pass
            error_count += 1
