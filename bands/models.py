from django.contrib.auth.models import User
from django.db import models

MAX_BANDNAME_LENGTH = 200


class Band(models.Model):
    name = models.CharField(max_length=MAX_BANDNAME_LENGTH)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
