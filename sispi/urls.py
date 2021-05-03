from django.urls import path, include
from rest_framework import routers
from django.urls import path, include
from .views.outputs import *
from .views.meta import *
from .views.utils import *
from .views.forecast_querys import ForecastViewSet

router = routers.SimpleRouter()
router.register('outputs', OutputModelViewSet)
router.register('meta/variables', MetVariabletModelViewSet)
router.register('meta/domains', DomainModelViewSet)
router.register('meta/provinces', ProvincesModelViewSet)
router.register('meta/municipalities', MunicipalitiesModelViewSet)

urlpatterns = (
    path(r'', include(router.urls)),
    path('init/provinces/', init_provinces_2, name='init_provinces'),
    path('forecast/', ForecastViewSet.as_view(), name='forecast_province'),
    path('forecast/<str:province>/', ForecastViewSet.as_view(), name='forecast_province'),

    path('utils/update_municipality/', update_municipality, name='update_municipality'),
    path('utils/update_municipality/', update_municipality, name='update_municipality'),
)

