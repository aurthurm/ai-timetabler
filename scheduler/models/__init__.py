from .simple_ga import *
from .complex_ga import *
from django.db import models


class GAType(models.Model):
    """
    Activate simple or complex GA
    """
    simple_ga = models.BooleanField(default=True)

    def __str__(self):
        return str(self.simple_ga)