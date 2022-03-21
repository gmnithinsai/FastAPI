import sys
sys.path.append('..')

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
import schemas, database, models, hash
from sqlalchemy.orm import Session

def create(request, db):
    new_user = models.User(username = request.username, email = request.email, password = hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'response':f'User has been created with name {request.username}'}

def get_all(response, db):
    all_users = db.query(models.User).all()
    if not all_users:
        response.status_code = status.HTTP_404_NOT_FOUND
    return all_users

def remove(id, db):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id:{id} is not available' )
    else:
        user.delete(synchronize_session=False)
    db.commit()
    return {'response':'user deleted'}
