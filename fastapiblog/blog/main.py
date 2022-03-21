from fastapi import FastAPI
from database import Base,engine
from routers import blogs, users, login

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(blogs.router)
