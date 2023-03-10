"""empty message

Revision ID: aa6a4923dcfd
Revises: 3b3580516928
Create Date: 2023-03-07 16:22:00.438749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa6a4923dcfd'
down_revision = '3b3580516928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cycle_predecessor_table',
    sa.Column('cycleBefore', sa.Integer(), nullable=False),
    sa.Column('cycleAfter', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('cycleBefore', 'cycleAfter')
    )
    op.create_table('subprocess_predecessor_table',
    sa.Column('subprocessBefore', sa.Integer(), nullable=False),
    sa.Column('subprocessAfter', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('subprocessBefore', 'subprocessAfter')
    )
    op.create_table('user_account_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('tokenGenerationTime', sa.DateTime(), nullable=False),
    sa.Column('emailVerificationStatus', sa.Boolean(), nullable=True),
    sa.Column('emailVerifiedTime', sa.DateTime(), nullable=True),
    sa.Column('roleType', sa.String(length=15), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('project_metrics_table',
    sa.Column('projectid', sa.Integer(), nullable=False),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('completeness', sa.Integer(), nullable=True),
    sa.Column('teamSize', sa.Integer(), nullable=True),
    sa.Column('teamMorale', sa.Integer(), nullable=True),
    sa.Column('teamWellness', sa.Integer(), nullable=True),
    sa.Column('timeframe', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user_account_table.id'], ),
    sa.PrimaryKeyConstraint('projectid')
    )
    op.create_table('cycle_table',
    sa.Column('cycleid', sa.Integer(), nullable=False),
    sa.Column('cycleRepeats', sa.Integer(), nullable=True),
    sa.Column('projectid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['projectid'], ['project_metrics_table.projectid'], ),
    sa.PrimaryKeyConstraint('cycleid')
    )
    op.create_table('git_commits_table',
    sa.Column('commitid', sa.Integer(), nullable=False),
    sa.Column('projectid', sa.Integer(), nullable=True),
    sa.Column('timeframe', sa.Integer(), nullable=True),
    sa.Column('numOfCommits', sa.Integer(), nullable=True),
    sa.Column('repoName', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['projectid'], ['project_metrics_table.projectid'], ),
    sa.ForeignKeyConstraint(['timeframe'], ['project_metrics_table.timeframe'], ),
    sa.PrimaryKeyConstraint('commitid')
    )
    op.create_table('subprocess_table',
    sa.Column('subprocessid', sa.Integer(), nullable=False),
    sa.Column('subprocessName', sa.String(length=100), nullable=True),
    sa.Column('cycleid', sa.Integer(), nullable=True),
    sa.Column('employeesRequired', sa.Integer(), nullable=False),
    sa.Column('costPerUnitTime', sa.Float(), nullable=True),
    sa.Column('completeness', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cycleid'], ['cycle_table.cycleid'], ),
    sa.PrimaryKeyConstraint('subprocessid')
    )
    op.create_table('probabilities_table',
    sa.Column('probabilityid', sa.Integer(), nullable=False),
    sa.Column('subprocessid', sa.Integer(), nullable=True),
    sa.Column('timeframe', sa.Integer(), nullable=True),
    sa.Column('probability', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['subprocessid'], ['subprocess_table.subprocessid'], ),
    sa.ForeignKeyConstraint(['timeframe'], ['project_metrics_table.timeframe'], ),
    sa.PrimaryKeyConstraint('probabilityid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('probabilities_table')
    op.drop_table('subprocess_table')
    op.drop_table('git_commits_table')
    op.drop_table('cycle_table')
    op.drop_table('project_metrics_table')
    op.drop_table('user_account_table')
    op.drop_table('subprocess_predecessor_table')
    op.drop_table('cycle_predecessor_table')
    # ### end Alembic commands ###
