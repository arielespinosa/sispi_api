from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sispi_api/v1.0/', include('sispi.urls'))
]
