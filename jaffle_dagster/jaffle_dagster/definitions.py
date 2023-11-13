import os

from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import jaffle_shop_dbt_assets, order_count_chart
from .constants import dbt_project_dir
from .schedules import schedules
from .sensors import customer_sensor

defs = Definitions(
    assets=[jaffle_shop_dbt_assets, order_count_chart],
    schedules=schedules,
    sensors=[customer_sensor],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)
