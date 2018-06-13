from xf.uc_dashboards.models.perspective import Perspective


def include_user_menu(request):

    if request.user.is_authenticated():

        if "perspective_id" in request.session:
            perspective = Perspective.objects.get(pk=request.session["perspective_id"])
        else:
            perspective = None

        request.user.load_perspectives()
        perspectives = request.user.perspectives
        return {'menu': "myMenu", 'perspectives':perspectives, 'current_perspective':perspective}
    else:
        return {}

