from fastapi import FastAPI, HTTPException, Depends #(depends tells fastapi thata fxn depends on another fxn or resource)
from sqlalchemy import text # wraps a raw sql qry so sqlclahcmy can execute it  
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas import UserRegistered, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, verify_access_token

from app.core.dependencies import get_current_user


app = FastAPI(title="AuthForge API")



@app.get("/health")
def health_check():
    return {"status":"healthy"}


@app.get("/db-check")
def databse_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 5+3"))

    return {"databse":result.scalar()}

######## user registeration 

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


######### user login

@app.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_data.email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



###### oauth

@app.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "email": current_user.email,
        "is_email_verified": current_user.is_email_verified
    }