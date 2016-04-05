from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class RaceCategory(models.Model):
    race = models.ForeignKey(Race)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.race.name


class Participant(models.Model):
     user = models.ForeignKey('authentication.CustomUser')
     race = models.ForeignKey(Race)
     category = models.ForeignKey(RaceCategory, blank=True, null=True)
     age = models.PositiveSmallIntegerField(blank=True, null=True)
     place = models.PositiveSmallIntegerField(blank=True, null=True)
     finish_time = models.DurationField(blank=True, null=True)
     avg_speed = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
     avg_pulse = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
     max_pulse = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
     cadence = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
     date_registered = models.DateField(auto_now_add=True)
     last_modified = models.DateField(auto_now=True)

     def __str__(self):
         return self.user.get_full_name()


class RaceTiming(models.Model):
    race = models.ForeignKey(Race)
    time_started = models.DateTimeField(auto_now_add=True)
    time_stopped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.race.name
