from django.contrib.auth.models import Group

def is_organiser(request):
    is_organiser = False
    if request.user.is_authenticated:
        is_organiser = Group.objects.filter(name='organisers', user=request.user).exists()
    return {'is_organiser': is_organiser}
