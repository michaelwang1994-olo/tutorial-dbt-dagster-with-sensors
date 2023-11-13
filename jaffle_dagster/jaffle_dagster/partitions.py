from dagster import StaticPartitionsDefinition, DynamicPartitionsDefinition, MultiPartitionsDefinition


static_partitions = StaticPartitionsDefinition(
    partition_keys=["a", "b", "c"]
)
dynamic_partitions = DynamicPartitionsDefinition(
    name="dynamic_partitions"
)
multi_partitions = MultiPartitionsDefinition({
    "static": static_partitions,
    "dynamic": dynamic_partitions
})