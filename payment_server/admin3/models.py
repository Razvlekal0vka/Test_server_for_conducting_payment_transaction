# models.py

from django.contrib.auth.models import User
from unfold.admin import ModelAdmin

@admin.register(User, site=custom_admin_site)
class UserAdmin(ModelAdmin):
    model = User