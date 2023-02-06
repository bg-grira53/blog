from mongoengine import Document , StringField , IntField

class Post(Document) :
    title = StringField(required=True)
    content = StringField(required=True)
    author = StringField(required=True)
    upvotes = IntField(default=0)
    downvotes = IntField(default=0)
