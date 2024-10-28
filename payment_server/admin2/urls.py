from .admin import admin2_site
from django.urls import path

urlpatterns = [
    path('', admin2_site.urls),
]
