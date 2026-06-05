import os
import dagster as dg
import dagster_dbt as dgdbt
from pathlib import Path

DBT_PROJECT_DIR = Path(__file__).resolve().parent.parent/'olist_transform'

@dgdbt.dbt_assets(manifest = os.path.join(DBT_PROJECT_DIR, 'target', 'manifest.json'))
def olist_transform_assets(context):
    yield from dgdbt.DbtCliResource(project_dir = DBT_PROJECT_DIR).cli(['build'], context = context).stream()

olist_transform_job = dg.define_asset_job(name = 'olist_transform_job', selection = '*')

olist_transform_schedule = dg.ScheduleDefinition(
    name = 'olist_daily_6am_schedule',
    job = olist_transform_job,
    cron_schedule = '0 6 * * *'
)
defs = dg.Definitions(
    assets = [olist_transform_assets],
    schedules = [olist_transform_schedule],
    resources = {'dbt':dgdbt.DbtCliResource(project_dir = DBT_PROJECT_DIR)}
    )