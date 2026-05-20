from django import forms

class PredictForm(forms.Form):
    user_name = forms.CharField(max_length=200, required=False)
    location = forms.CharField(max_length=200, required=False)
    area_sqft = forms.FloatField(required=True)
    bedrooms = forms.IntegerField(required=True)
    bathrooms = forms.IntegerField(required=True)
    year_built = forms.IntegerField(required=False)
