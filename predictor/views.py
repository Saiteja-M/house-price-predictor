from django.shortcuts import render
import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings

# Home page
def home(request):
    return render(request, 'predictor/home.html')



# ✅ Load your model
model_path = os.path.join(settings.BASE_DIR, "predictor", "ml", "artifacts", "house_price_model.joblib")
model = joblib.load(model_path)

def home(request):
    return render(request, 'predictor/home.html')  # your form page


def predict_price(request):
    if request.method == 'POST':
        area_type = request.POST.get('area_type')
        availability = request.POST.get('availability')
        location = request.POST.get('location')
        size = request.POST.get('size')
        society = request.POST.get('society', 'Unknown')
        total_sqft = float(request.POST.get('total_sqft', 0))
        bath = float(request.POST.get('bath', 0))
        balcony = float(request.POST.get('balcony', 0))

        # ✅ Create a DataFrame with proper column names
        input_data = pd.DataFrame([{
            'area_type': area_type,
            'availability': availability,
            'location': location,
            'size': size,
            'society': society,
            'total_sqft': total_sqft,
            'bath': bath,
            'balcony': balcony
        }])

        # ✅ Predict using DataFrame
        predicted_price = model.predict(input_data)[0]

        return render(request, 'predictor/result.html', {'predicted_price': predicted_price})
    
    return render(request, 'predictor/home.html')
import os, csv
from django.shortcuts import render
from django.conf import settings
from .forms import PredictForm
from .models import HouseInput
from .model_loader import get_model
from django.contrib import messages

CSV_DIR = os.path.join(settings.BASE_DIR, "data")
CSV_PATH = os.path.join(CSV_DIR, "user_inputs.csv")

def ensure_csv_header(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","user_name","location","area_sqft","bedrooms","bathrooms","year_built","predicted_price"])

def append_input_to_csv(path, row):
    ensure_csv_header(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def predict_view(request):
    form = PredictForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        # Prepare features (adapt to your model's expected order)
        features = [data.get("area_sqft") or 0, data.get("bedrooms") or 0, data.get("bathrooms") or 0, data.get("year_built") or 0]

        model = get_model()
        try:
            pred_value = float(model.predict([features])[0])
        except Exception as e:
            pred_value = 0.0
            messages.error(request, f"Model prediction failed; returning 0.0. Error: {e}")

        # Save to DB first (so we have record id and timestamp)
        house = HouseInput.objects.create(
            user_name = data.get("user_name"),
            location = data.get("location"),
            area_sqft = data.get("area_sqft"),
            bedrooms = data.get("bedrooms"),
            bathrooms = data.get("bathrooms"),
            year_built = data.get("year_built"),
            predicted_price = pred_value,
            input_as_json = data
        )

        # Append to CSV for analytics (best-effort)
        row = [house.created_at.isoformat(), house.user_name, house.location,
               house.area_sqft, house.bedrooms, house.bathrooms, house.year_built, house.predicted_price]
        try:
            append_input_to_csv(CSV_PATH, row)
        except Exception:
            # don't fail the request if CSV write fails
            pass

        # Pass saved object and prediction to template
        context.update({
            "saved": True,
            "house": house,
            "prediction": pred_value,
        })

        return render(request, "predictor/result.html", context)

    return render(request, "predictor/predict.html", context)
from django.http import HttpResponse, FileResponse

from django.contrib.admin.views.decorators import staff_member_required
import os
from django.conf import settings

@staff_member_required
def download_export(request):
    path = os.path.join(settings.BASE_DIR, "data", "user_inputs.csv")
    if not os.path.exists(path):
        return HttpResponse("CSV not found. Run export first.", status=404)
    return FileResponse(open(path,'rb'), as_attachment=True, filename="user_inputs.csv")
