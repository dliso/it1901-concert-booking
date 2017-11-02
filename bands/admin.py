from django.contrib import admin
from django.shortcuts import HttpResponseRedirect
from rules.contrib.admin import ObjectPermissionsModelAdmin

from . import models

admin.site.register(models.Band)
admin.site.register(models.Genre)
admin.site.register(models.Festival)
admin.site.register(models.Offer)

class TechnicalNeedAdmin(ObjectPermissionsModelAdmin):
    def response_change(self, request, obj):
        return HttpResponseRedirect(obj.concert_name.get_absolute_url())

admin.site.register(models.TechnicalNeed, TechnicalNeedAdmin)

class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage_size', 'num_seats')

admin.site.register(models.Stage, StageAdmin)

class TechnicalNeedInline(admin.StackedInline):
    model = models.TechnicalNeed
    max_num = 1

class ConcertAdmin(ObjectPermissionsModelAdmin):
    inlines = [
        TechnicalNeedInline
    ]

admin.site.register(models.Concert, ConcertAdmin)
