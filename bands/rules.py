from django.contrib.auth.models import Group
from rules import add_perm, always_allow, always_deny, is_superuser, predicate

from . import models
from .groups import Groups


@predicate
def is_manager(user, obj):
    if not obj:
        return False
    return user == obj.band.manager


@predicate
def is_concert_booker(user):
    return user.groups.filter(name=Groups.CONCERT_BOOKERS.value).exists()


@predicate
def is_a_manager(user):
    for b in models.Band.objects.all():
        if b.manager == user:
            return True
    return False

@predicate
def is_chief_booker(user):
    return user.groups.filter(name=Groups.CHIEF_BOOKERS.value).exists()


is_booker = is_chief_booker | is_concert_booker

add_perm('offer.view', is_concert_booker)
add_perm('offerlist.view', is_booker)
add_perm('offermanager.view', is_a_manager)

add_perm('bands', always_allow)
# add_perm('bands.add_technicalneed', is_superuser | is_manager)
add_perm('bands.change_technicalneed', is_manager)
# add_perm('bands.delete_technicalneed', is_superuser | is_manager)

add_perm('band.manage', is_manager)

add_perm('stage.view_econ_report', is_booker)

add_perm('concert.book', is_booker)
add_perm('concert.edit', is_chief_booker)
add_perm('concert.edit_tech_staff', is_booker)

add_perm('offer.view', is_booker | is_manager)
add_perm('offer.create', is_booker)
add_perm('offer.approve', is_chief_booker)
add_perm('offer.accept', always_deny)

add_perm('booking.view', is_booker | is_manager)
add_perm('booking.view_dashboard', is_booker)
