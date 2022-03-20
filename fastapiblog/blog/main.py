from fastapi import FastAPI
from database import Base,engine
from routers import blogs, users


app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(users.router, blogs.router)
