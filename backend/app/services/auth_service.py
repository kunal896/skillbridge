from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.auth import RegisterRequest
from app.utils.security import hash_password,verify_password
def register(db:Session,payload:RegisterRequest)->Account:
    if db.scalar(select(Account).where(Account.email==payload.email.lower())): raise ValueError("Email already registered")
    account=Account(email=payload.email.lower(),password_hash=hash_password(payload.password),role=payload.role)
    db.add(account); db.commit(); db.refresh(account); return account
def authenticate(db:Session,email:str,password:str)->Account|None:
    a=db.scalar(select(Account).where(Account.email==email.lower()))
    return a if a and verify_password(password,a.password_hash) else None
