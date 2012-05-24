from google.appengine.api import users
from django.utils.functional import SimpleLazyObject

__author__ = 'jez'

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = users.get_current_user()
    return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.user = SimpleLazyObject(lambda: get_user(request))