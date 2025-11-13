from django.core.management.base import BaseCommand
import csv
from dataentry.utils import check_csv_errors

# Proposed command - python manage.py importData <file_path> <model_name>


class Command(BaseCommand):
    help = "Inserts data from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file.")
        parser.add_argument("model", type=str, help="Name of the table.")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model"].capitalize()

        model = check_csv_errors(file_path, model_name)

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for data in reader:
                model.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully."))
