from django.db import models

MAX_BANDNAME_LENGTH = 200


class Band(models.Model):
    name = models.CharField(max_length=MAX_BANDNAME_LENGTH)
