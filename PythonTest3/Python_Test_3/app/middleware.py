from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from datetime import datetime

class RequestMiddleware(MiddlewareMixin):
    def process_request(self,request):
        timestamp = datetime.now()

        print('requested url',request.path)
        print('timestamp: ',timestamp)

        response = self.get_response(request)

        return response

