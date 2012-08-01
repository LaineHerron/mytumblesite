from mongoengine import *
import datetime


class User(Document):

    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=30)
    email = StringField(max_length=30)


class Comment(EmbeddedDocument):

    author = ReferenceField(User)
    content = StringField(max_length=120, required=True)
    created_at = DateTimeField(default=datetime.datetime.now,
                               required=True)
    meta = {'ordering': ['-created_at']}


class Post(Document):

    author = ReferenceField(User)
    title = StringField(required=True, max_length=50)
    content = StringField(max_length=120)
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.datetime.now,
                               required=True)
    meta = {'ordering': ['-created_at']}


current_user = None

