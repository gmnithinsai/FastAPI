import uvicorn
from typing import Optional
from fastapi import FastAPI
from blog.schemas import Blog

app = FastAPI()
@app.post('/blog')
def create_blog(request:Blog):
    return {'data': f'blog was created with title {request.title}'}
@app.get('/blog')
def index(limit=10, published:bool=True, sort:Optional[str]=None):
    if published:
        return {'data': f'{limit} Published blogs available'}
    else:
        return {'data':f'{limit} blogs available'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'unpublished  blogs'}

@app.get("/blog/{id}")
def blog(id:int):
    return {'data':id}

@app.get("/blog/{id}/comments")
def comments(id):
    return {'data':{'comments':'This is comment'}}


# if __name__ == '__main__':
#     uvicorn.run(app)