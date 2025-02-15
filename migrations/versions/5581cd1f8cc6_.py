"""empty message

Revision ID: 5581cd1f8cc6
Revises: d645a619f279
Create Date: 2022-08-12 19:28:37.403397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5581cd1f8cc6'
down_revision = 'd645a619f279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(), nullable=True))
    op.add_column('Artist', sa.Column('looking_for_venues', sa.Boolean(), nullable=False))
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=False))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=250), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'looking_for_talent')
    op.drop_column('Venue', 'website_link')
    op.drop_column('Artist', 'looking_for_venues')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###
