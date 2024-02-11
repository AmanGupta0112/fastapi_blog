from blog import schemas,models
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

def get_user(db:Session, username: str):
    return db.query(models.User).filter(models.User.email == username).first()
    
    
def get_all(db:Session):
    return db.query(models.Blog).all()

def create(request:schemas.Blog,db:Session,get_current_user:schemas.User):
    user = get_user(db,get_current_user)
    new_blog = models.Blog(title=request.title, body=request.body,user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def destroy(id:int,db:Session,get_current_user:schemas.User):
    user = get_user(db,get_current_user)
    blog = db.query(models.Blog).filter(models.Blog.id == id , models.Blog.user_id == user.id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found!!",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done!!"

def show(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found!!",
        )
    return blog

def update(id:int,request:schemas.Blog,db:Session,get_current_user:schemas.User):
    user = get_user(db,get_current_user)
    blog = db.query(models.Blog).filter(models.Blog.id == id , models.Blog.user_id == user.id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found!!",
        )
    blog.update(dict(request), synchronize_session=False)
    db.commit()

    return "update successfully!!"