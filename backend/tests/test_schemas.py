from app.schemas.auth import RegisterRequest
from app.schemas.roadmap import RoadmapCreate,RoadmapStepCreate
def test_register_schema(): assert RegisterRequest(email='a@example.com',password='password123').role=='learner'
def test_roadmap_schema():
    r=RoadmapCreate(target_role='Data Analyst',steps=[RoadmapStepCreate(skill='SQL',title='SQL',description='Basics',reason='Demand',step_order=1)]); assert r.steps[0].skill=='SQL'
