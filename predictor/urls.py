from django.urls import path
from . import views  # ✅ import your views file

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_price, name='predict_price'),
    path("", views.predict_view, name="predict"),
    path("admin/export-download/", views.download_export, name="export-download")

]

