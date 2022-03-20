from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from .. import schemas, database, models, hash
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, tags=['user'])
def create_user(request:schemas.User, db:Session=Depends(database.get_db)):
    new_user = models.User(username = request.username, email = request.email, password = hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'response':f'User has been created with name {request.username}'}

@router.get('/user', status_code = status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['user'])
def get_all_users(response: Response, db:Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    if not all_users:
        response.status_code = status.HTTP_404_NOT_FOUND
    return all_users

@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
def remove_user_by_id(id, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id:{id} is not available' )
    else:
        user.delete(synchronize_session=False)
    db.commit()
    return {'response':'user deleted'}