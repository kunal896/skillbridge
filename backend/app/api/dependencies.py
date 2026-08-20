from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.account import Account
from app.utils.security import decode_access_token
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def get_current_account(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)) -> Account:
    err=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token", headers={"WWW-Authenticate":"Bearer"})
    try: account_id=UUID(decode_access_token(token)["sub"])
    except (KeyError,ValueError,jwt.InvalidTokenError): raise err
    account=db.scalar(select(Account).where(Account.id==account_id))
    if account is None: raise err
    return account


def get_optional_account(
    token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)),
    db: Session = Depends(get_db),
) -> Account | None:
    if not token:
        return None
    try:
        account_id = UUID(decode_access_token(token)["sub"])
    except (KeyError, ValueError, jwt.InvalidTokenError):
        return None
    return db.scalar(select(Account).where(Account.id == account_id))
