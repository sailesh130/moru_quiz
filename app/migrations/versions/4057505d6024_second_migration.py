"""second migration.

Revision ID: 4057505d6024
Revises: 5885057db953
Create Date: 2023-04-13 17:55:13.423570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4057505d6024'
down_revision = '5885057db953'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_profile', schema=None) as batch_op:
        batch_op.drop_constraint('quiz_profile_user_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_profile', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('quiz_profile_user_fkey', 'question', ['user'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###
