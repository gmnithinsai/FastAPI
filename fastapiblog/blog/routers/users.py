import sys
sys.path.append('..')

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
import schemas, database, models, hash
from sqlalchemy.orm import Session
from repository import users


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User, db:Session=Depends(database.get_db)):
    return users.create(request,db)

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[schemas.ShowUser] )
def get_all_users(response: Response, db:Session = Depends(database.get_db)):
    return users.get_all(response, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT )
def remove_user_by_id(id, db:Session = Depends(database.get_db)):
    return users.remove(id,db)
    