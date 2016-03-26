from .models import Race
from django.shortcuts import get_object_or_404


class CheckRaceExistenceMixin(object):
    def initial(self, *args, **kwargs):
        queryset = Race.objects.filter(id=kwargs['race_pk'])
        get_object_or_404(queryset)
        return super(CheckRaceExistenceMixin, self).initial(*args, **kwargs)