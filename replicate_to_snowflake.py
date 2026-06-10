import pandas as pd
import sqlalchemy as sqa
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

engine = sqa.create_engine('postgresql+psycopg2://postgres:vincent23@localhost/olist_project')

with engine.connect() as con:
    result = con.execute(sqa.text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'raw_%';"))
    tables = [row[0] for row in result]

if not tables:
    print('No staging tables found in PostgreSQL. Ensure ingestion ran first')
    exit(1)

ctx = snowflake.connector.connect(
    user = 'PEGI',
    password = 'ytdEMbAL8iuCvzw',
    account = 'DCWKBGQ-QH90954',
    warehouse = 'ENGINEERING_WH',
    database = 'olist_project',
    schema = 'PUBLIC',
    role = 'engineering_role'
)

cursor = ctx.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS olist_project;")
cursor.execute(f"USE DATABASE olist_project;")
cursor.execute(f"USE SCHEMA PUBLIC;")

for table in tables:
    with engine.connect() as conn:
        df = pd.read_sql_table(table, con = conn)
    df.columns = [c.upper() for c in df.columns]
    sf_table_name = table.upper()
    success, nchunks, nrows, _ = write_pandas(
        conn = ctx,
        df = df,
        table_name = sf_table_name,
        auto_create_table = True
    )
    
    if success:
        print(f"Successfully loaded {nrows} rows into Snowflake!\n")
    else:
        print(f"Failed loading table {sf_table_name}\n")

cursor.close()
ctx.close()
print('Cloud replication layer processing complete')

