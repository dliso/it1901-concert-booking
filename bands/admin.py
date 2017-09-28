from django.contrib import admin

from . import models

admin.site.register(models.Band)
admin.site.register(models.Genre)
admin.site.register(models.Concert)

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage_size', 'num_seats')

admin.site.register(models.Stage, StageAdmin)
