from django.contrib import admin
from .models.outputs import *
from .models.meta import *

admin.site.register(MetVariable)
admin.site.register(Forecast)
admin.site.register(PointLocation)
admin.site.register(RunOutput)
admin.site.register(Domain)
