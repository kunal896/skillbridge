from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.schemas.employer import EmployerCreate,EmployerRead,EmployerRequirementCreate,EmployerRequirementRead
from app.services.employer_service import profile,by_account,requirement
router=APIRouter(prefix="/employers",tags=["employers"])
@router.put("/me",response_model=EmployerRead)
def my_company(p:EmployerCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    if a.role!="employer":raise HTTPException(403,"Employer account required")
    return profile(db,a.id,p)
@router.post("/requirements",response_model=EmployerRequirementRead)
def req(p:EmployerRequirementCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    if a.role!="employer":raise HTTPException(403,"Employer account required")
    e=by_account(db,a.id)
    if not e:raise HTTPException(404,"Employer profile not found")
    return requirement(db,e.id,p)
