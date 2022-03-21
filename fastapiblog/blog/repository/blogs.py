import sys
sys.path.append('..')

from fastapi import status, Depends, HTTPException, Response
import schemas, database, models
from sqlalchemy.orm import Session


def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request:schemas.Blog,db:Session):
    # username = data.username
    # user = db.query(models.User).filter(username = username).first()
    new_blog = models.Blog(title = request.title, description = request.description, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_blog(id, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} is not available' )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id:{id} is not available'}
    return blog

def remove(id,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} is not available' )
    else:
        blog.delete(synchronize_session=False)
    db.commit()
    return {'Response': 'Blog deleted succesfully!'}

def update(id,request, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id:{id} not found')
    else:
        blog.update({'title':request.title, 'description':request.description}, synchronize_session='evaluate')
    db.commit()
    return {'response':'Blog has been updated!', 'updated post': request}

