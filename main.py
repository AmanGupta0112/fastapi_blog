from fastapi import FastAPI
from blog import database, models
from blog.routers import blog,user,login

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)



