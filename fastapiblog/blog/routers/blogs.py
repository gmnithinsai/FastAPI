import sys
sys.path.append('..')

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
import schemas, database, oauth
from sqlalchemy.orm import Session
from repository import blogs

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_blog(request:schemas.Blog, db:Session=Depends(database.get_db),get_current_user:schemas.User=Depends(oauth.get_current_user)):
    
    return blogs.create(request, db)


@router.get('/', status_code = status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session = Depends(database.get_db), get_current_user:schemas.User=Depends(oauth.get_current_user)):
    return blogs.get_all(db)

@router.get('/{id}', status_code = 200, response_model=schemas.ShowBlog )
def get_blog_by_id(id, db:Session = Depends(database.get_db), get_current_user:schemas.User=Depends(oauth.get_current_user)):
    return blogs.get_blog(id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT )
def remove_blog_by_id(id, db:Session = Depends(database.get_db), get_current_user:schemas.User=Depends(oauth.get_current_user)):
    return blogs.remove(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED )
def update_blog(id, request:schemas.Blog, db:Session = Depends(database.get_db), get_current_user:schemas.User=Depends(oauth.get_current_user)):
    return blogs.update(id, request, db)



