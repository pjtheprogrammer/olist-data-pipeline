import os
from dagster import Definitions, ScheduleDefinition, define_asset_job
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

# This tells Dagster where your dbt project lives (the current folder)
dbt_project_dir = Path(__file__).parent.absolute()

@dbt_assets(manifest=dbt_project_dir / "target/manifest.json")
def olist_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

olist_dbt_job = define_asset_job(name="olist_dbt_job", selection="*")

olist_dbt_schedule = ScheduleDefinition(
    job=olist_dbt_job,
    cron_schedule="0 0 * * *", 
)

defs = Definitions(
    assets=[olist_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)