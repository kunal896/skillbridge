import json,uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.roadmap import Roadmap,RoadmapStep
from app.schemas.roadmap import RoadmapCreate
def create(db:Session,learner_id:uuid.UUID,p:RoadmapCreate)->Roadmap:
    r=Roadmap(learner_id=learner_id,target_role=p.target_role,overall_summary=p.overall_summary); db.add(r); db.flush()
    for i,s in enumerate(p.steps,1): db.add(RoadmapStep(roadmap_id=r.id,skill=s.skill,title=s.title,description=s.description,reason=s.reason,step_order=s.step_order,status="unlocked" if i==1 else "locked",citations_json=json.dumps(s.citations)))
    db.commit(); db.refresh(r); return r
def get(db:Session,roadmap_id):
    r=db.get(Roadmap,roadmap_id)
    if not r:return None,[]
    steps=list(db.scalars(select(RoadmapStep).where(RoadmapStep.roadmap_id==roadmap_id).order_by(RoadmapStep.step_order)).all())
    return r,steps
