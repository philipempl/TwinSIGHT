import os
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, CsvTableSink, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Rowtime, Json, Kafka, Elasticsearch
from pyflink.table.window import Tumble

def register_transactions_source(st_env):
    st_env.connect(Kafka()
                   .version("universal")
                   .topic("transactions-data")
                   .start_from_latest()
                   .property("zookeeper.connect", "host.docker.internal:2181")
                   .property("bootstrap.servers", "host.docker.internal:19091")) \
        .with_format(Json()
        .fail_on_missing_field(True)
        .schema(DataTypes.ROW([
        DataTypes.FIELD("customer", DataTypes.STRING()),
        DataTypes.FIELD("transaction_type", DataTypes.STRING()),
        DataTypes.FIELD("online_payment_amount", DataTypes.DOUBLE()),
        DataTypes.FIELD("in_store_payment_amount", DataTypes.DOUBLE()),
        DataTypes.FIELD("lat", DataTypes.DOUBLE()),
        DataTypes.FIELD("lon", DataTypes.DOUBLE()),
        DataTypes.FIELD("transaction_datetime", DataTypes.TIMESTAMP())]))) \
        .with_schema(Schema()
        .field("customer", DataTypes.STRING())
        .field("transaction_type", DataTypes.STRING())
        .field("online_payment_amount", DataTypes.DOUBLE())
        .field("in_store_payment_amount", DataTypes.DOUBLE())
        .field("lat", DataTypes.DOUBLE())
        .field("lon", DataTypes.DOUBLE())
        .field("rowtime", DataTypes.TIMESTAMP())
        .rowtime(
        Rowtime()
            .timestamps_from_field("transaction_datetime")
            .watermarks_periodic_bounded(60000))) \
        .in_append_mode() \
        .register_table_source("source")
        
def register_transactions_es_sink(st_env):
    st_env.connect(Elasticsearch()
                   .version("6")
                   .host("0.0.0.0", 9200, "http")
                   .index("transactions-supermarket-case")
                   .document_type("usage")) \
        .with_schema(Schema()
                     .field("customer", DataTypes.STRING())
                     .field("count_transactions", DataTypes.STRING())
                     .field("total_online_payment_amount", DataTypes.DOUBLE())
                     .field('total_in_store_payment_amount', DataTypes.DOUBLE())
                     .field("lon", DataTypes.FLOAT())
                     .field("lat", DataTypes.FLOAT())
                     .field('last_transaction_time', DataTypes.STRING())
                     ) \
        .with_format(Json().derive_schema()).in_upsert_mode().register_table_sink("sink_elasticsearch")
        
def transactions_job():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_parallelism(1)
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    st_env = StreamTableEnvironment \
        .create(s_env, environment_settings=EnvironmentSettings
                .new_instance()
                .in_streaming_mode()
                .use_blink_planner().build())

    register_transactions_source(st_env)
    register_transactions_es_sink(st_env)

    st_env.from_path("source") \
        .window(Tumble.over("10.hours").on("rowtime").alias("w")) \
        .group_by("customer, w") \
        .select("""customer as customer, 
                   count(transaction_type) as count_transactions,
                   sum(online_payment_amount) as total_online_payment_amount, 
                   sum(in_store_payment_amount) as total_in_store_payment_amount,
                   last(lat) as lat,
                   last(lon) as lon,
                   w.end as last_transaction_time
                   """) \
        .filter("total_online_payment_amount<total_in_store_payment_amount") \ 
        .filter("count_transactions>=3") \
        .filter("lon < 20.62") \ .filter("lon > 20.20") \
        .filter("lat < 44.91") \ .filter("lat > 44.57") \
        .insert_into("sink_into_csv")

    st_env.execute("app")


if __name__ == '__main__':
    usage_job()