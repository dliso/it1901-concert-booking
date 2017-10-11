from django.contrib import admin

from . import models

admin.site.register(models.Band)
admin.site.register(models.Genre)
admin.site.register(models.Festival)
admin.site.register(models.TechnicalNeed)

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage_size', 'num_seats')

admin.site.register(models.Stage, StageAdmin)

class TechnicalNeedInline(admin.StackedInline):
    model = models.TechnicalNeed
    max_num = 1

class ConcertAdmin(admin.ModelAdmin):
    inlines = [
        TechnicalNeedInline
    ]

admin.site.register(models.Concert, ConcertAdmin)
