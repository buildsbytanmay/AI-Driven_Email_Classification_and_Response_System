from fastapi import FastAPI
from app.database import Base, engine

# import models so SQLAlchemy registers them
from app.models import email, reply_history

# import routers
from app.routers import auth
from app.routers import email_routes
from app.routers import reply_routes

from app.routers import email_routes, history_routes


# FIRST create app
app = FastAPI()

# Then include routers
app.include_router(auth.router)
app.include_router(email_routes.router)
app.include_router(reply_routes.router)

app.include_router(email_routes.router)
app.include_router(history_routes.router)

# Create tables in database
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI Email Assistant Backend Running"}