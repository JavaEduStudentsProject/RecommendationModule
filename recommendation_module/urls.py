from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('recommendation_module_api.urls')),
    path('admin/', admin.site.urls),
]
