from fastapi import FastAPI, HTTPException, Depends #(depends tells fastapi thata fxn depends on another fxn or resource)
from sqlalchemy import text # wraps a raw sql qry so sqlclahcmy can execute it  
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas import UserRegistered
from app.core.security import hash_password

app = FastAPI(title="AuthForge API")

@app.get("/health")
def health_check():
    return {"status":"healthy"}


@app.get("/db-check")
def databse_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 5+3"))

    return {"databse":result.scalar()}


@app.post("/auth/register")
def register(user_data: UserRegistered, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user :
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

