from fastapi import FastAPI, Depends #(depends tells fastapi thata fxn depends on another fxn or resource)
from sqlalchemy import text # wraps a raw sql qry so sqlclahcmy can execute it  
from sqlalchemy.orm import Session

from app.db.session import get_db

app = FastAPI(title="AuthForge API")

@app.get("/health")
def health_check():
    return {"status":"healthy"}


@app.get("/db-check")
def databse_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 5+3"))

    return {"databse":result.scalar()}