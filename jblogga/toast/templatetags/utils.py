import datetime
from django import template
from google.appengine.api import users

register = template.Library()

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%M-%D")

class EditableBlogNode(template.Node):

    def __init__(self, author):
        self.author = template.Variable(author)

    def render(self, context):
        actual_author = self.author.resolve(context)
        context['can_edit'] = users.is_current_user_admin() or (users.get_current_user() == actual_author.author)
        return ''

@register.tag
def get_is_editable(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, author= token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return EditableBlogNode(author)

