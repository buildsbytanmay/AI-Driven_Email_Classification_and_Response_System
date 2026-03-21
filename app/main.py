from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

# import models so SQLAlchemy registers them
from app.models import email, reply_history

app = FastAPI()
app.include_router(auth.router)

# Create tables in database
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI Email Assistant Backend Running"}