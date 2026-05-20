# predictor/management/commands/export_inputs.py
from django.core.management.base import BaseCommand
import csv
import os
from predictor.models import HouseInput
from django.conf import settings

class Command(BaseCommand):
    help = "Export HouseInput rows to data/user_inputs.csv"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, default=os.path.join(settings.BASE_DIR, "data", "user_inputs.csv"))

    def handle(self, *args, **options):
        path = options["path"]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Location","Area_sqft","Bedrooms","Bathrooms","Predicted_Price","Date"])
            for h in HouseInput.objects.all().order_by("created_at"):
                writer.writerow([h.location, h.area_sqft, h.bedrooms, h.bathrooms, h.predicted_price, h.created_at])
        self.stdout.write(self.style.SUCCESS(f"Exported {HouseInput.objects.count()} rows to {path}"))
