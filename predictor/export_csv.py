import csv
from predictor.models import HouseInput

def export_to_csv():
    with open("data/user_inputs.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Location", "Area (sqft)", "Bedrooms", "Bathrooms", "Predicted Price", "Date"])
        for h in HouseInput.objects.all():
            writer.writerow([
                h.location,
                h.area_sqft,
                h.bedrooms,
                h.bathrooms,
                h.predicted_price,
                h.created_at
            ])
    print("✅ Exported to data/user_inputs.csv successfully!")
