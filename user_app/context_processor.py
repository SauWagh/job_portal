# user_app/context_processors.py
from .models import UserDetail  # adjust if your model is in another app

def user_profile(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = request.user.detail  # or your related_name
        except UserDetail.DoesNotExist:
            profile = None
    return {'profile': profile}
