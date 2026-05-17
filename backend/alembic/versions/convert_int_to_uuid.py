"""convert int PK/FK to UUID strings

Revision ID: convert_int_to_uuid
Revises: 25586723bd55
Create Date: 2026-05-17 00:00:00.000000

This migration is a scaffold/template. It performs the following high-level steps:
- For each affected table, add a new temporary `new_id` (String) column.
- Populate `new_id` with UUIDs for each existing row (using Python's uuid4 in a DB-agnostic way).
- For each foreign-key column referencing the table's old integer PK, add a temporary `new_<fk>` column,
  populate it by mapping old FK -> new_id via joins.
- Once all new columns are populated, drop old FK constraints/columns and rename new columns to the canonical names.

WARNING: This is a potentially destructive migration for production databases. BACK UP your DB before running.
Review and test carefully. You may prefer to perform this migration offline with application downtime.

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.sql import table, column, select

# revision identifiers, used by Alembic.
revision = 'convert_int_to_uuid'
down_revision = '25586723bd55'
branch_labels = None
depends_on = None

# Tables to convert and their foreign keys mapping.
# Format: table_name: { 'pk': 'id', 'fks': { 'other_table': [('fk_column', 'referencing_column'), ...] } }
# NOTE: Fill or adjust this mapping to match your schema before running the migration.
TABLES = {
    'users': { 'pk': 'id', 'fks': {} },
    'workspaces': { 'pk': 'id', 'fks': { 'users': [('user_id', 'id')] } },
    'subjects': { 'pk': 'id', 'fks': { 'workspaces': [('workspace_id', 'id')] } },
    'documents': { 'pk': 'id', 'fks': { 'subjects': [('subject_id', 'id')] } },
    'chunks': { 'pk': 'id', 'fks': { 'documents': [('document_id', 'id')] } },
    'research_profiles': { 'pk': 'id', 'fks': { 'users': [('user_id', 'id')] } },
}


def upgrade() -> None:
    conn = op.get_bind()

    # 1) Add new_id columns
    for tbl, meta in TABLES.items():
        op.add_column(tbl, sa.Column('new_id', sa.String(length=36), nullable=True))

    # 2) Populate new_id with generated UUIDs per row (DB-agnostic, done in Python)
    for tbl, meta in TABLES.items():
        pk = meta['pk']
        rows = conn.execute(sa.text(f"SELECT {pk} FROM {tbl}")).fetchall()
        for (old_pk,) in rows:
            new_uuid = str(uuid.uuid4())
            conn.execute(sa.text(f"UPDATE {tbl} SET new_id = :nid WHERE {pk} = :old"), {'nid': new_uuid, 'old': old_pk})

    # 3) For each FK referencing table, add temporary fk columns and populate by joining on old integer IDs
    for tbl, meta in TABLES.items():
        # find fks in other tables that reference this table
        for other_tbl, other_meta in TABLES.items():
            for fk_col, ref_col in other_meta.get('fks', {}).get(tbl, []) if other_meta.get('fks') else []:
                # add new column on other_tbl
                new_fk_col = f'new_{fk_col}'
                op.add_column(other_tbl, sa.Column(new_fk_col, sa.String(length=36), nullable=True))
                # populate by joining other_tbl.<fk_col> -> tbl.<pk>
                conn.execute(sa.text(
                    f"UPDATE {other_tbl} SET {new_fk_col} = (SELECT new_id FROM {tbl} WHERE {tbl}.{meta['pk']} = {other_tbl}.{fk_col}) WHERE {other_tbl}.{fk_col} IS NOT NULL"
                ))

    # 4) Drop old FK constraints, drop old PK/FK columns, and rename new columns into place.
    # This section is intentionally left as comments and guidance because constraint names vary by DB and deployment.
    # TODO: Replace the guidance below with explicit `op.drop_constraint`, `op.drop_column`, and `op.alter_column` calls
    # for your database and environment.

    # Example (Postgres):
    # op.drop_constraint('workspaces_user_id_fkey', 'workspaces', type_='foreignkey')
    # op.drop_column('workspaces', 'user_id')
    # op.alter_column('workspaces', 'new_user_id', new_column_name='user_id', nullable=False)

    # For primary keys, you will need to:
    # - drop dependent FK constraints first
    # - drop the PK constraint
    # - drop old integer PK column
    # - alter/rename new_id -> id and create new PK

    # Because constraint names and sequences differ, finish this migration manually.


def downgrade() -> None:
    # Downgrade is non-trivial and potentially unsafe. Manual steps required to restore integer IDs.
    raise NotImplementedError('Downgrade is not implemented for convert_int_to_uuid migration.')