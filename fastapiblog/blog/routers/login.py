import sys
sys.path.append('..')

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database, hash, JWTtoken
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/login',
    tags=['Login']
)

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Username!')
    password = hash.verify_password(user.password, request.password)

    if not password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password!')
    
    
    access_token = JWTtoken.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


    


