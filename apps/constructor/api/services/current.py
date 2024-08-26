from rest_framework.views import Request
from apps.profiles.models import Profile
from apps.constructor.models import Contest


def get_current_contest(request: Request) -> int:
    try:
        section = get_current_section(request)
        return Contest.objects.get(section=section)
    except:
        raise Exception("contest is not selected")

def get_current_section(request: Request):
    return Profile.objects.get(user=request.user).section
