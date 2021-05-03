from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models.outputs import RunOutput, Forecast
from .models.meta import Municipality


def forecast_municipality(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action is "post_add":
        forecast = Forecast.objects.get(pk=pk_set)
        for municipality in Municipality.objects.filter(geom__isnull=False):
            points = [point.pk for point in municipality.domain_points(1)]

            for point in points:
                f = forecast.forecast['point'] == point


            if municipality.geom:
                points = None


        print("Voy a guardar las variables")
        print(sender)
        print(instance)
        print(reverse)
        print(model)
        print(pk_set)
        print(kwargs)

    pass


#m2m_changed.connect(forecast_municipality, RunOutput.forecast.through)
