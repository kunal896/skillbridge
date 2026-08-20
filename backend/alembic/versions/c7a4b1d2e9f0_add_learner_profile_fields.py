"""add learner profile skill fields"""
from alembic import op
import sqlalchemy as sa

revision = "c7a4b1d2e9f0"
down_revision = "b05e26de1aeb"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("learners", sa.Column("skills_json", sa.Text(), nullable=False, server_default="[]"))
    op.add_column("learners", sa.Column("verified_skills_json", sa.Text(), nullable=False, server_default="[]"))
    op.add_column("learners", sa.Column("experience_years", sa.Integer(), nullable=True))
    op.add_column("learners", sa.Column("education", sa.Text(), nullable=True))
    op.alter_column("learners", "skills_json", server_default=None)
    op.alter_column("learners", "verified_skills_json", server_default=None)

def downgrade():
    op.drop_column("learners", "education")
    op.drop_column("learners", "experience_years")
    op.drop_column("learners", "verified_skills_json")
    op.drop_column("learners", "skills_json")
