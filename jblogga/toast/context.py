from google.appengine.api import users

__author__ = 'jez'

def google_auth_urls(request):
    """
    context processor to return google auth login/logout urls
    """
    return { "auth_urls" : { "in" : users.create_login_url("/"), "out" : users.create_logout_url("/") }}



