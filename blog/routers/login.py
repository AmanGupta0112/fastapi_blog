from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from blog import schemas,models,database,hashing,tokens
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated

get_db = database.get_db


router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post("/")
def login(request:Annotated[OAuth2PasswordRequestForm, Depends()],db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {request.username} not found!!",
        )
    
    if not hashing.Hash().verify(user.password,request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials!!",
        )
    
    access_token = tokens.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
    
