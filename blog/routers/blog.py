from fastapi import APIRouter,Depends,status
from blog import schemas,database,oauth2
from sqlalchemy.orm import Session
from typing import List
from blog.repository import blog


get_db = database.get_db
router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.create(request,db,get_current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.destroy(id,db,get_current_user)



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_blog(id: int, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.show(id,db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.update(id,request,db,get_current_user)