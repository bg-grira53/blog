from fastapi import FastAPI , HTTPException , Body

from mongoengine import connect ,Q
from mongoengine.errors import DoesNotExist
from fastapi.middleware.cors import CORSMiddleware
import json 

from models import Post

mongodb_uri = "mongodb+srv://bayrem:4LBEkzs5zP0rRpIQ@cluster0.3jfvxrn.mongodb.net/?retryWrites=true&w=majority"


connect(
    db='blog',
    host= mongodb_uri
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def main():

    posts = Post.objects.all()
    return [{"id": str(post.id), "title": post.title, "content": post.content, "author": post.author, "upvotes": post.upvotes, "downvotes": post.downvotes} for post in posts]



@app.get("/get_post/{post_id}")
async def get_post_by_id(post_id : str ):
   
    try:
        post = Post.objects.get(id=post_id)
        return {"id": str(post.id), "title": post.title, "content": post.content, "author": post.author, "upvotes": post.upvotes, "downvotes": post.downvotes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/post")
async def create_ppst(preview: dict = Body(...)):
    try:
        post = Post(**preview)
        print(post)
        post.save()
        return {"message": "Post added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.put("/post/{vote}/{post_id}")
async def handle_vote( vote : str , post_id: str):
    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        return {"error": "Blog not found"}

    if vote == "upvote":
        post.upvotes += 1
    elif vote == "downvote":
        post.downvotes += 1
    else:
        return {"error": "Invalid vote type"}

    post.save()
    return {"message": "Vote registered successfully"}


@app.get("/post/search")
async def search_posts(q: str):
    posts = Post.objects(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__icontains=q))
    return [{"id": str(post.id), "title": post.title, "content": post.content, "author": post.author, "upvotes": post.upvotes, "downvotes": post.downvotes} for post in posts]