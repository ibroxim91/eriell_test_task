from threading import current_thread

from django.utils.deprecation import MiddlewareMixin


_requests = {}


# Получаем текущий запрос
def current_request():
    return _requests.get(current_thread().ident, None)


class MyRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _requests[current_thread().ident] = request

    def process_response(self, request, response):
       # когда ответ готов, запрос должен быть сброшен
        _requests.pop(current_thread().ident, None)
        return response


    def process_exception(self, request, exception):
        # если произошло исключение, запрос тоже должен быть сброшен
         _requests.pop(current_thread().ident, None)
