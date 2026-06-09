import os
from dagster import Definitions
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

# This tells Dagster where your dbt project lives (the current folder)
dbt_project_dir = Path(__file__).parent.absolute()

@dbt_assets(manifest=dbt_project_dir / "target/manifest.json")
def olist_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

defs = Definitions(
    assets=[olist_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)