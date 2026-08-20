import json,uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.employer import Employer,EmployerRequirement
from app.schemas.employer import EmployerCreate,EmployerRequirementCreate
def profile(db:Session,account_id:uuid.UUID,p:EmployerCreate):
    x=db.scalar(select(Employer).where(Employer.account_id==account_id))
    if x is None:x=Employer(account_id=account_id,**p.model_dump());db.add(x)
    else:x.company_name=p.company_name;x.description=p.description
    db.commit();db.refresh(x);return x
def by_account(db:Session,account_id:uuid.UUID):return db.scalar(select(Employer).where(Employer.account_id==account_id))
def requirement(db:Session,employer_id:uuid.UUID,p:EmployerRequirementCreate):
    x=EmployerRequirement(employer_id=employer_id,role_title=p.role_title,region=p.region,required_skills_json=json.dumps(p.required_skills),description=p.description);db.add(x);db.commit();db.refresh(x);return x
