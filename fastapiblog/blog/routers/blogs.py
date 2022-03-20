from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session
router = APIRouter()


@router.post('/blog', status_code = status.HTTP_201_CREATED, tags=['blog'])
def create_blog(request:schemas.Blog, db:Session=Depends(database.get_db)):
    new_blog = models.Blog(title = request.title, description = request.description, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog', status_code = status.HTTP_200_OK, response_model=List[schemas.ShowBlog],tags=['blog'])
def get_all_blogs(response: Response, db:Session = Depends(database.get_db)):
    all_blogs = db.query(models.Blog).all()
    if not all_blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
    return all_blogs

@router.get('/blog/{id}', status_code = 200, response_model=schemas.ShowBlog, tags=['blog'])
def get_blog_by_id(id, response:Response, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} is not available' )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id:{id} is not available'}
    return blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def remove_blog_by_id(id, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} is not available' )
    else:
        blog.delete(synchronize_session=False)
    db.commit()
    return {'Response': 'Blog deleted succesfully!'}

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id, request:schemas.Blog, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id:{id} not found')
    else:
        blog.update({'title':request.title, 'description':request.description}, synchronize_session='evaluate')
    db.commit()
    return {'response':'Blog has been updated!', 'updated post': request}
