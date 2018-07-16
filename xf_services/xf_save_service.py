from django.contrib.auth.models import User
from django.http import HttpRequest


class XFSaveService():

    @classmethod
    def get_user(cls) -> User:

        # See https://stackoverflow.com/questions/32332329/getting-the-request-user-form-pre-save-in-django
        import inspect

        request: HttpRequest = None
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break

        return request.user if request is not None else None

