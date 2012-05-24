from django.conf.urls.defaults import *
from jblogga.toast.views import HomeView, AddBlogEntryView, ViewBlogEntryView, DeleteBlogEntryView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^jbongga/', include('jbongga.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view()),
    url(r'^add$', AddBlogEntryView.as_view()),
    url(r'^blog/(?P<key>[\d\w-]+)$', ViewBlogEntryView.as_view()),
    url(r'^delete/(?P<key>[\d\w-]+)$', DeleteBlogEntryView.as_view()),
)
