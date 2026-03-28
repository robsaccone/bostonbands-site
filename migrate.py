#!/usr/bin/env python3
"""Migrate Azure SQL database to local PostgreSQL."""

import pymssql
import psycopg2
import psycopg2.extras
import sys
import uuid

MIGRATIONS = [
    {
        "mssql": {"server": "YOUR_SERVER.database.windows.net", "user": "YOUR_USER", "password": "YOUR_PASSWORD", "database": "YOUR_DATABASE", "login_timeout": 10, "tds_version": "7.3"},
        "pg": {"host": "localhost", "port": 5433, "user": "postgres", "password": "YOUR_PG_PASSWORD", "dbname": "your_target_db"},
    },
]

# SQL Server to PostgreSQL type mapping
TYPE_MAP = {
    "int": "INTEGER",
    "bigint": "BIGINT",
    "smallint": "SMALLINT",
    "tinyint": "SMALLINT",
    "bit": "BOOLEAN",
    "float": "DOUBLE PRECISION",
    "real": "REAL",
    "decimal": "NUMERIC({precision},{scale})",
    "numeric": "NUMERIC({precision},{scale})",
    "money": "NUMERIC(19,4)",
    "smallmoney": "NUMERIC(10,4)",
    "char": "CHAR({length})",
    "nchar": "CHAR({length})",
    "varchar": "TEXT",
    "nvarchar": "TEXT",
    "text": "TEXT",
    "ntext": "TEXT",
    "datetime": "TIMESTAMPTZ",
    "datetime2": "TIMESTAMPTZ",
    "smalldatetime": "TIMESTAMPTZ",
    "date": "DATE",
    "time": "TIME",
    "datetimeoffset": "TIMESTAMPTZ",
    "uniqueidentifier": "UUID",
    "varbinary": "BYTEA",
    "binary": "BYTEA",
    "image": "BYTEA",
    "xml": "TEXT",
}


def get_pg_type(col):
    """Map a SQL Server column type to PostgreSQL."""
    t = col["type"].lower()
    template = TYPE_MAP.get(t, "TEXT")
    if "{precision}" in template:
        return template.format(precision=col["precision"], scale=col["scale"])
    if "{length}" in template:
        return template.format(length=col["length"])
    return template


def get_tables(mssql_cur):
    """Get all user tables from dbo schema."""
    mssql_cur.execute("""
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'
        ORDER BY TABLE_NAME
    """)
    return [row[0] for row in mssql_cur.fetchall()]


def get_columns(mssql_cur, table):
    """Get column info for a table."""
    mssql_cur.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH,
               NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = %s AND TABLE_SCHEMA = 'dbo'
        ORDER BY ORDINAL_POSITION
    """, (table,))
    cols = []
    for row in mssql_cur.fetchall():
        cols.append({
            "name": row[0].lower(),
            "type": row[1],
            "length": row[2] or 0,
            "precision": row[3] or 0,
            "scale": row[4] or 0,
            "nullable": row[5] == "YES",
        })
    return cols


def get_primary_keys(mssql_cur, table):
    """Get primary key columns for a table."""
    mssql_cur.execute("""
        SELECT c.COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE c
            ON tc.CONSTRAINT_NAME = c.CONSTRAINT_NAME
        WHERE tc.TABLE_NAME = %s AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
        ORDER BY c.COLUMN_NAME
    """, (table,))
    return [row[0].lower() for row in mssql_cur.fetchall()]


psycopg2.extras.register_uuid()


def migrate_db(mssql_config, pg_config):
    db_name = mssql_config["database"]
    print(f"\n{'='*60}")
    print(f"Migrating {db_name}...")
    print(f"{'='*60}")

    print("Connecting to Azure SQL...")
    mssql_conn = pymssql.connect(**mssql_config)
    mssql_cur = mssql_conn.cursor()

    print("Connecting to PostgreSQL...")
    pg_conn = psycopg2.connect(**pg_config)
    pg_conn.autocommit = False
    pg_cur = pg_conn.cursor()

    tables = get_tables(mssql_cur)
    print(f"Found {len(tables)} tables: {', '.join(tables)}")

    for table in tables:
        pg_table = table.lower()
        columns = get_columns(mssql_cur, table)
        pks = get_primary_keys(mssql_cur, table)

        # Drop and create table
        pg_cur.execute(f'DROP TABLE IF EXISTS "{pg_table}" CASCADE')

        col_defs = []
        for col in columns:
            pg_type = get_pg_type(col)
            nullable = "" if col["nullable"] else " NOT NULL"
            col_defs.append(f'  "{col["name"]}" {pg_type}{nullable}')

        if pks:
            col_defs.append(f'  PRIMARY KEY ({", ".join(f"{k}" for k in pks)})')

        create_sql = f'CREATE TABLE "{pg_table}" (\n' + ",\n".join(col_defs) + "\n)"
        pg_cur.execute(create_sql)

        # Copy data
        mssql_cur.execute(f"SELECT * FROM [{table}]")
        col_names = ", ".join(f'"{c["name"]}"' for c in columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert_sql = f'INSERT INTO "{pg_table}" ({col_names}) VALUES ({placeholders})'

        batch = []
        count = 0
        for row in mssql_cur:
            values = []
            for i, val in enumerate(row):
                ctype = columns[i]["type"].lower()
                if ctype == "bit" and val is not None:
                    val = bool(val)
                elif ctype == "uniqueidentifier" and val is not None:
                    val = str(val) if not isinstance(val, str) else val
                values.append(val)
            batch.append(tuple(values))
            count += 1
            if len(batch) >= 1000:
                pg_cur.executemany(insert_sql, batch)
                batch = []

        if batch:
            pg_cur.executemany(insert_sql, batch)

        pg_conn.commit()
        print(f"  {pg_table}: {count} rows migrated")

    mssql_cur.close()
    mssql_conn.close()
    pg_cur.close()
    pg_conn.close()
    print(f"\n{db_name} migration complete!")


if __name__ == "__main__":
    try:
        for m in MIGRATIONS:
            migrate_db(m["mssql"], m["pg"])
        print("\nAll migrations complete!")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
