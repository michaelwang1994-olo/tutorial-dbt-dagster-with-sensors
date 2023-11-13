from dagster import multi_asset_sensor, MultiAssetSensorEvaluationContext, EventLogEntry, AssetKey, AssetSelection, define_asset_job, RunRequest, SensorResult
from .partitions import multi_partitions, static_partitions, dynamic_partitions


run_order_count_chart = define_asset_job(
    name="order_count_chart_job",
    selection=AssetSelection.keys(AssetKey("order_count_chart")),
    partitions_def=multi_partitions
)


@multi_asset_sensor(
    monitored_assets=[AssetKey("customers")],
    job=run_order_count_chart,
    minimum_interval_seconds=60
)
def customer_sensor(context: MultiAssetSensorEvaluationContext):
    asset_events = context.latest_materialization_records_by_key()
    context.log.info(asset_events)
    dynamic_partition_add_requests = []
    run_requests = []
    for dynamic_partition in ["1", "2", "3"]:
        dynamic_partition_add_requests.append(dynamic_partitions.build_add_request([dynamic_partition]))
        for static_partition in static_partitions.get_partition_keys():
            run_requests.append(RunRequest(run_key=f"{dynamic_partition}|{static_partition}", partition_key=f"{dynamic_partition}|{static_partition}"))
        # run_requests.append(RunRequest(run_key=f"{static_partition}", partition_key=f"{static_partition}"))
    context.advance_all_cursors()
    return SensorResult(
        run_requests=run_requests,
        dynamic_partitions_requests=dynamic_partition_add_requests,
        cursor=context.cursor
    )
