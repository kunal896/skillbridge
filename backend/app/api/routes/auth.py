from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import RegisterRequest,LoginRequest,TokenResponse
from app.services.auth_service import register,authenticate
from app.utils.security import create_access_token
router=APIRouter(prefix="/auth",tags=["auth"])
@router.post("/register",response_model=TokenResponse,status_code=status.HTTP_201_CREATED)
def register_account(p:RegisterRequest,db:Session=Depends(get_db)):
    try:a=register(db,p)
    except ValueError as e:raise HTTPException(status_code=409,detail=str(e))
    return TokenResponse(access_token=create_access_token(str(a.id),a.role),account_id=a.id,role=a.role)
@router.post("/login",response_model=TokenResponse)
def login(p:LoginRequest,db:Session=Depends(get_db)):
    a=authenticate(db,p.email,p.password)
    if not a:raise HTTPException(status_code=401,detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(a.id),a.role),account_id=a.id,role=a.role)
