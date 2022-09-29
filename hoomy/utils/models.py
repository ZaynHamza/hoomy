import uuid

from django.db import models


class Entity(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(editable=True, auto_now_add=True)
    updated = models.DateTimeField(editable=True, auto_now=True)
