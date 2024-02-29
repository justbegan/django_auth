from ..models import Profile
from ..serializers import Profile_serializer


def get_profile(request):
    obj = Profile.objects.get(user=request.user.id)
    ser = Profile_serializer(obj)
    return ser.data
