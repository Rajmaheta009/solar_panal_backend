"""sync

Revision ID: 4237351225bd
Revises: e8d0094764d7
Create Date: 2024-12-22 18:01:31.902528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4237351225bd'
down_revision: Union[str, None] = 'e8d0094764d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_pages_content_id', table_name='pages_content')
    op.drop_table('pages_content')
    op.drop_index('ix_menu_id', table_name='menu')
    op.drop_table('menu')
    op.drop_index('ix_auth_user_id', table_name='auth_user')
    op.drop_table('auth_user')
    op.drop_index('ix_contact_us_email', table_name='contact_us')
    op.drop_index('ix_contact_us_id', table_name='contact_us')
    op.drop_index('ix_contact_us_name', table_name='contact_us')
    op.drop_table('contact_us')
    op.drop_index('ix_application_id', table_name='application')
    op.drop_table('application')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_name', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_pages_id', table_name='pages')
    op.drop_table('pages')
    op.drop_index('ix_news_id', table_name='news')
    op.drop_table('news')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('picture', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='news_pkey')
    )
    op.create_index('ix_news_id', 'news', ['id'], unique=False)
    op.create_table('pages',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('pages_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('menu_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], name='pages_menu_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='pages_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_pages_id', 'pages', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phonenumber', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_name', 'users', ['name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_table('application',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('InnerHtmlText', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='application_pkey')
    )
    op.create_index('ix_application_id', 'application', ['id'], unique=False)
    op.create_table('contact_us',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ph_no', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='contact_us_pkey')
    )
    op.create_index('ix_contact_us_name', 'contact_us', ['name'], unique=False)
    op.create_index('ix_contact_us_id', 'contact_us', ['id'], unique=False)
    op.create_index('ix_contact_us_email', 'contact_us', ['email'], unique=True)
    op.create_table('auth_user',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], name='auth_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='auth_user_pkey')
    )
    op.create_index('ix_auth_user_id', 'auth_user', ['id'], unique=False)
    op.create_table('menu',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('menu_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='menu_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_menu_id', 'menu', ['id'], unique=False)
    op.create_table('pages_content',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], name='pages_content_page_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='pages_content_pkey')
    )
    op.create_index('ix_pages_content_id', 'pages_content', ['id'], unique=False)
    # ### end Alembic commands ###
