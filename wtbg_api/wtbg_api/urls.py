from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('wtbg_api_module/', include('wtbg_api_module.urls')),
]
