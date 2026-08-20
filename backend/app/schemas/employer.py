from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class EmployerCreate(BaseModel):
    company_name:str=Field(min_length=1,max_length=200); description:str|None=None
class EmployerRead(EmployerCreate):
    id:UUID; account_id:UUID; created_at:datetime
class EmployerRequirementCreate(BaseModel):
    role_title:str=Field(min_length=1,max_length=160); region:str|None=None; required_skills:list[dict]=[]; description:str|None=None
class EmployerRequirementRead(EmployerRequirementCreate):
    id:UUID; employer_id:UUID; created_at:datetime
