"""Initial schema creation.

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema."""
    # Create companies table
    op.create_table(
        'companies',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('ticker', sa.String(10), nullable=True),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('risk_score_updated_at', sa.DateTime(), nullable=False),
        sa.Column('executive_summary', sa.Text(), nullable=True),
        sa.Column('summary_updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', name='uq_companies_ticker'),
    )
    op.create_index('idx_company_name', 'companies', ['name'])
    op.create_index('idx_company_ticker', 'companies', ['ticker'])

    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('sentiment_label', sa.String(20), nullable=True),
        sa.Column('entities', sa.JSON(), nullable=True),
        sa.Column('embedding_id', sa.String(100), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('ingested_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_document_company', 'documents', ['company_id'])
    op.create_index('idx_document_source', 'documents', ['source'])
    op.create_index('idx_document_published', 'documents', ['published_at'])

    # Create risk_scores table
    op.create_table(
        'risk_scores',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('rule_score', sa.Float(), nullable=True),
        sa.Column('ml_score', sa.Float(), nullable=True),
        sa.Column('features', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_risk_score_company', 'risk_scores', ['company_id'])
    op.create_index('idx_risk_score_created', 'risk_scores', ['created_at'])

    # Create watchlists table
    op.create_table(
        'watchlists',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_watchlist_user', 'watchlists', ['user_id'])

    # Create watchlist_items table
    op.create_table(
        'watchlist_items',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('watchlist_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('added_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['watchlist_id'], ['watchlists.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('watchlist_id', 'company_id', name='uq_watchlist_company'),
    )
    op.create_index('idx_watchlist_item_watchlist', 'watchlist_items', ['watchlist_id'])
    op.create_index('idx_watchlist_item_company', 'watchlist_items', ['company_id'])

    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('watchlist_id', sa.String(36), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_triggered_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['watchlist_id'], ['watchlists.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_alert_user', 'alerts', ['user_id'])
    op.create_index('idx_alert_watchlist', 'alerts', ['watchlist_id'])

    # Create sentiment_timeseries table
    op.create_table(
        'sentiment_timeseries',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('avg_sentiment', sa.Float(), nullable=False),
        sa.Column('document_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('positive_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('negative_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('neutral_count', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'date', name='uq_sentiment_company_date'),
    )
    op.create_index('idx_sentiment_company', 'sentiment_timeseries', ['company_id'])
    op.create_index('idx_sentiment_date', 'sentiment_timeseries', ['date'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index('idx_sentiment_date', table_name='sentiment_timeseries')
    op.drop_index('idx_sentiment_company', table_name='sentiment_timeseries')
    op.drop_table('sentiment_timeseries')
    op.drop_index('idx_alert_watchlist', table_name='alerts')
    op.drop_index('idx_alert_user', table_name='alerts')
    op.drop_table('alerts')
    op.drop_index('idx_watchlist_item_company', table_name='watchlist_items')
    op.drop_index('idx_watchlist_item_watchlist', table_name='watchlist_items')
    op.drop_table('watchlist_items')
    op.drop_index('idx_watchlist_user', table_name='watchlists')
    op.drop_table('watchlists')
    op.drop_index('idx_risk_score_created', table_name='risk_scores')
    op.drop_index('idx_risk_score_company', table_name='risk_scores')
    op.drop_table('risk_scores')
    op.drop_index('idx_document_published', table_name='documents')
    op.drop_index('idx_document_source', table_name='documents')
    op.drop_index('idx_document_company', table_name='documents')
    op.drop_table('documents')
    op.drop_index('idx_company_ticker', table_name='companies')
    op.drop_index('idx_company_name', table_name='companies')
    op.drop_table('companies')

