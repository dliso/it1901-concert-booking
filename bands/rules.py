from . import models
from rules import add_perm, always_deny, always_allow, predicate, is_superuser

@predicate
def is_manager(user, tech_need):
    if not tech_need:
        return False
    print(tech_need)
    print(tech_need.concert_name)
    print(tech_need.concert_name.band_name.manager)
    return user == tech_need.concert_name.band_name.manager


add_perm('bands', always_allow)
# add_perm('bands.add_technicalneed', is_superuser | is_manager)
add_perm('bands.change_technicalneed', is_superuser | is_manager)
# add_perm('bands.delete_technicalneed', is_superuser | is_manager)
