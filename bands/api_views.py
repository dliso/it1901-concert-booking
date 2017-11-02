from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rules.contrib.views import PermissionRequiredMixin

from . import forms, models


def occurrences(request):
    start = request.GET['start']
    end = request.GET['end']

    concerts = models.Concert.objects.filter(
        concert_time__gte=start,
        concert_time__lte=end
    )

    return JsonResponse(
        [c.json() for c in concerts],
        safe=False
    )
