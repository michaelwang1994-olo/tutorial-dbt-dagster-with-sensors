from dagster import OpExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
import os

import duckdb
import pandas as pd
import plotly.express as px
from dagster import MetadataValue, AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model
from .partitions import multi_partitions, static_partitions

from .constants import dbt_manifest_path, dbt_project_dir
duckdb_database_path = dbt_project_dir.joinpath("tutorial.duckdb")


@dbt_assets(manifest=dbt_manifest_path)
def jaffle_shop_dbt_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()



@asset(
    compute_kind="python",
    deps=get_asset_key_for_model([jaffle_shop_dbt_assets], "customers"),
    # partitions_def=static_partitions,
    partitions_def=multi_partitions
)
def order_count_chart(context):
    # read the contents of the customers table into a Pandas DataFrame
    connection = duckdb.connect(os.fspath(duckdb_database_path))
    customers = connection.sql("select * from customers").df()

    # create a plot of number of orders by customer and write it out to an HTML file
    fig = px.histogram(customers, x="number_of_orders")
    fig.update_layout(bargap=0.2)
    save_chart_path = duckdb_database_path.parent.joinpath("order_count_chart.html")
    fig.write_html(save_chart_path, auto_open=True)

    # tell Dagster about the location of the HTML file,
    # so it's easy to access from the Dagster UI
    context.add_output_metadata(
        {"plot_url": MetadataValue.url("file://" + os.fspath(save_chart_path))}
    )
