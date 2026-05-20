# predictor/admin.py
from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import HouseInput

# Admin action to export selected rows as CSV
@admin.action(description="Export selected HouseInputs to CSV")
def export_as_csv(modeladmin, request, queryset):
    field_names = ["location", "area_sqft", "bedrooms", "bathrooms", "predicted_price", "created_at"]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=houseinputs_export.csv"
    writer = csv.writer(response)
    writer.writerow([f.replace("_", " ").title() for f in field_names])
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in field_names])
    return response

@admin.register(HouseInput)
class HouseInputAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "area_sqft", "bedrooms", "bathrooms", "predicted_price", "created_at")
    list_filter = ("location", "created_at")
    search_fields = ("location", "user_name")
    actions = [export_as_csv]
