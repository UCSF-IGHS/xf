from django.utils.deprecation import MiddlewareMixin


class LoginMenuMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response


    def process_request(self, request):
        #print("Middleware executed")
        pass


