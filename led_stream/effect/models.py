from django.db import models


class LedStream(models.Model):
    # Defines what effect the LedEffect is currently running
    led_effect: models.IntegerField()
