from django.urls import path, include
from rest_framework import routers
from django.urls import path, include
from .views.outputs import *
from .views.meta import *
from .views.forecast_querys import ForecastViewSet
from .views.init_netcdf2database import NetCDF2DataBase


router = routers.SimpleRouter()
router.register('outputs', OutputModelViewSet)
router.register('meta/variables', MetVariabletModelViewSet)
router.register('meta/domains', DomainModelViewSet)
router.register('meta/provinces', ProvincesModelViewSet)
router.register('meta/municipalities', MunicipalitiesModelViewSet)

urlpatterns = (
    path(r'', include(router.urls)),
    path('init/netcdf_2_database/', NetCDF2DataBase.as_view(), name='netcdf_2_database'),
    path('forecast/', ForecastViewSet.as_view(), name='forecast_province'),
    path('forecast/<str:province>/', ForecastViewSet.as_view(), name='forecast_province'),
)

