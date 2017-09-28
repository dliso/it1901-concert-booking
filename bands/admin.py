from django.contrib import admin

from . import models

admin.site.register(models.Band)
admin.site.register(models.Genre)
admin.site.register(models.Stage)
admin.site.register(models.Concert)
