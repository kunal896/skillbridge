from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
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
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    account = authenticate(
        db,
        form_data.username,
        form_data.password,
    )

    if account is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        str(account.id),
        account.role,
    )

    return TokenResponse(
        access_token=token,
        account_id=account.id,
        role=account.role,
    )
