from django.urls import path, include

urlpatterns = [
    path('admin1/', include('admin1.urls')),
    path('admin2/', include('admin2.urls')),
]
