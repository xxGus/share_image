from mongoengine import (
    Document,
    ReferenceField,
    StringField)

from .user import User

class DashboardUser(Document):
    birthday = StringField()
    gender = StringField()
    user = ReferenceField(User)
