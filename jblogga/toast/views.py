# Create your views here.
from django.http import Http404

from django.views.generic.edit import FormView
from jblogga.toast.forms import DeleteBlogEntryForm

from models import BlogEntry
from forms import AddBlogEntryForm
from django.views.generic import TemplateView, View



class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """
        add recent blog entries
        """
        context = super(HomeView, self).get_context_data(**kwargs)
        context['blogs'] = [entry for entry in BlogEntry.all_recent()]

        return context

class AddBlogEntryView(FormView):
    template_name = "addnew.html"
    form_class = AddBlogEntryForm
    success_url = '/'

    def form_valid(self, form):
        """
        save the blog and delegate back up to formview for the redirect
        """
        BlogEntry.put_blog(self.request.user,form.cleaned_data['title'],form.cleaned_data['body'])
        return super(AddBlogEntryView, self).form_valid(form)

class ViewBlogEntryView(TemplateView):
    template_name = "full_blog_entry.html"

    def get_context_data(self, **kwargs):
        """
        add recent blog entries
        """
        context = super(ViewBlogEntryView, self).get_context_data(**kwargs)
        blog = BlogEntry.get_blog(kwargs['key'])

        if not blog:
            raise Http404

        context['blog'] = blog

        return context

class DeleteBlogEntryView(FormView):
    template_name = "delete.html"
    form_class = DeleteBlogEntryForm
    success_url = "/"

    def get_initial(self):
        return {'key' : self.kwargs['key']}

    def get_context_data(self, **kwargs):
        """
        fetch the blog that is about to be deleted
        """
        context = super(DeleteBlogEntryView, self).get_context_data(**kwargs)
        blog = BlogEntry.get_blog(self.kwargs['key'])

        if not blog:
            raise Http404

        context['blog'] = blog

        return context

    def form_valid(self, form):
        """
        save the blog and delegate back up to formview for the redirect
        """
        BlogEntry.delete_blog(form.cleaned_data['key'])
        return super(DeleteBlogEntryView, self).form_valid(form)









