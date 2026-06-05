from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import olist_transform_dbt_assets
from .project import olist_transform_project
from .schedules import schedules

defs = Definitions(
    assets=[olist_transform_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=olist_transform_project),
    },
)

