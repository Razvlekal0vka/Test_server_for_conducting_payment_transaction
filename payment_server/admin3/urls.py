# urls.py

from django.urls import path
from .sites import custom_admin_site

urlpatterns = [
    # other URL patterns
    path("admin/", custom_admin_site.urls),
]