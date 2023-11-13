A clone of: https://github.com/dbt-labs/jaffle_shop

Note that jaffle_shop/jaffle_dagster/sensors.py contains an `asset_sensor` that creates runs a downstream dynamic partition job. 
The error that I am trying to highlight is that when the sensor is run, the following things happen:
1. Before the upstream dbt assets have materialized the sensor behaves as expected and returns "No new materialization events found for asset key AssetKey(['customers'])"
2. Right after the upstream dbt assets have materialized, the sensor behaves as expected and runs, adding ["1", "2", "3"] as dynamic partitions and requesting 9 partition run requests
3. However, every time after first sensor tick runs, the subsequent sensor ticks execute the code within the sensor and tries to launch 9 more partition run requests before.
   
    i. the partition materializations are not executed because they share the same run key as the previous partition materialization
