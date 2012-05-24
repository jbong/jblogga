import datetime
from google.appengine.ext import db
from google.appengine.ext.db import BadKeyError


class BlogEntry(db.Model):
    author = db.UserProperty()
    title = db.StringProperty()
    body = db.TextProperty()
    created_at = db.DateTimeProperty()

    @classmethod
    def all_recent(cls):
        q = BlogEntry.all()
        q.order('-created_at')
        return q.fetch(5)

    @classmethod
    def put_blog(cls, author, title, body):
        blog_entry = BlogEntry(author=author, title=title, body=body, created_at=datetime.datetime.now())
        blog_entry.put()

    @classmethod
    def get_blog(cls, key):
        try:
            return db.get(key)
        except BadKeyError:
            return None

    @classmethod
    def delete_blog(cls, key):
        db.delete(key)