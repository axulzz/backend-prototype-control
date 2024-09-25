import os

from django.core.management.base import BaseCommand, CommandError
from apps.cores.models import AcademicLevel


class Command(BaseCommand):
    help = "create academic levels"

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "..", "carrees_list.txt")
        if not os.path.isfile(file_path):
            raise CommandError(f"The file {file_path} does not exist.")

        try:
            with open(file_path, "r") as file:
                file_content = file.read().split("\n")

                for academicLevelObj in file_content:
                    AcademicLevel.objects.create(text=academicLevelObj)

                self.stdout.write(self.style.SUCCESS("created, Ok"))

        except IOError as e:
            raise CommandError(f"Error reading the file: {e}")
