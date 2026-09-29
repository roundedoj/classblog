from .permissions import is_author


def author_status(request):
    return {'is_author': is_author(request.user)}