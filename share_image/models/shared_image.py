from datetime import datetime

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DateTimeField)

from .dashboard_user import DashboardUser

class SharedImage(Document):
    path = StringField()
    user = ReferenceField(DashboardUser)
    created_at = DateTimeField(required=True, default=datetime.now)