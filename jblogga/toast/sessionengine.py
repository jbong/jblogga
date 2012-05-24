from time import timezone
import uuid
from django.utils.encoding import force_unicode
from google.appengine.ext import db
from django.contrib.sessions.backends.base import SessionBase

__author__ = 'jez'

class Session(db.Model):
    session_key = db.StringProperty()
    session_data = db.TextProperty()
    expire_date = db.DateTimeProperty()

    def get_decoded(self):
        return SessionStore().decode(self.session_data)


class SessionStore(SessionBase):
    """
    Simple session engine that uses google datastore
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def get_session_entity_key(self):
        if not self._session_key:
            return None
        #return db.Key.from_path('Session', self._session_key)
        return self._session_key

    def _get_new_session_key(self):
        """
        using a guid as the key (minus the hyphen's)
        """
        return str(uuid.uuid1()).replace('-','')

    def load(self):

        session_k = self.get_session_entity_key()
        session = db.get(session_k)

        if session and (session.expire_date > timezone.now()):
            return self.decode(force_unicode(session.session_data))
        else:
            # session not found
            self.create()
            return {}

    def exists(self, session_key):
        return db.get(self.get_session_entity_key()) is not None

    def create(self):

        self._session_key = self._get_new_session_key()
        try:
           # Save immediately to ensure we have a unique entry in the
           # database.
           self.save(must_create=True)
        except Exception, e:
            pass

        self.modified = True
        self._session_cache = {}
        return

    def save(self, must_create=False):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).

        Or not..this is my munged version...
        """
        key = self._get_or_create_session_key()

        session = Session(
            key_name=key,
            session_key=key,
            session_data=self.encode(self._get_session(no_load=must_create)),
            expire_date=self.get_expiry_date()
        )
        session.put()


    def delete(self, session_key=None):
        if not session_key:
            return

        session_k = self.get_session_entity_key()
        db.delete(session_k)

