
from django.db import models


class ClicOh(models.Model):

    remove = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

