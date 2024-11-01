# sites.py
from django.contrib import admin
from unfold.sites import UnfoldAdminSite

class CustomAdminSite(UnfoldAdminSite):
    pass


custom_admin_site = CustomAdminSite(name="custom_admin_site")