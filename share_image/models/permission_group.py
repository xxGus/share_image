
import datetime
from bson.objectid import ObjectId
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    IntField,
    ObjectIdField,
    ReferenceField,
    StringField,
)

class PermissionGroup(Document):
    can_access_backoffice = BooleanField(default=False)
    can_access_dashboard = BooleanField(default=False)
    name = StringField(required=True)

    @property
    def permitted(self):
        lst = []
        attrs = self.to_mongo().to_dict()
        for key in attrs:
            if "can_" in key and attrs[key]:
                lst.append(key)
        return lst