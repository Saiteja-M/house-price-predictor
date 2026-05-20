from django.db import models
from django.db import models

class HouseInput(models.Model):
    # user-provided fields (change to match your app)
    user_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    area_sqft = models.FloatField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)

    # prediction/result
    predicted_price = models.FloatField(null=True, blank=True)

    # analytics / metadata
    input_as_json = models.JSONField(null=True, blank=True)  # raw features, requires Postgres (supports JSONField)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} | {self.area_sqft} sqft | ₹{self.predicted_price}"


# Create your models here.
