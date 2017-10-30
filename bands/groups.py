from enum import Enum, unique

from django.contrib.auth.models import Group

@unique
class Groups(Enum):
    AUDIO_TECHS = 'audio_technicians'
    LIGHT_TECHS = 'light_technicians'
    CONCERT_ARRANGERS = 'concert_arrangers'
    CONCERT_BOOKERS = 'concert_bookers'
    CHIEF_BOOKERS = 'chief_bookers'
    PR_MANAGERS = 'pr_managers'
