from datetime import datetime

from mongoengine import (
    BooleanField,
    Document,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ReferenceField,
    StringField)

from .permission_group import PermissionGroup

class Email(EmbeddedDocument):
    validated = BooleanField(required=True, default=False)
    value = StringField(required=True)

class User(Document):
    name = StringField()
    password = StringField()
    email = EmbeddedDocumentField(Email)
    permissions = ReferenceField(PermissionGroup)
