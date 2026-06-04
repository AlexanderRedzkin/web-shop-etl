#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum as spark_sum, round
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

def main():
    spark = SparkSession.builder \
        .appName("Sales ETL") \
        .master("local[*]") \
        .getOrCreate()

    schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("date", StringType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("price", DoubleType(), True),
        StructField("customer_id", IntegerType(), True)
    ])

    input_path = "/opt/spark/data/raw/*.csv"
    df = spark.read.csv(input_path, header=True, schema=schema)

    df = df.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
    df = df.withColumn("total_price", round(col("quantity") * col("price"), 2))

    daily_revenue = df.groupBy("date").agg(
        round(spark_sum("total_price"), 2).alias("revenue")
    )

    output_path = "/opt/spark/data/processed/daily_revenue.parquet"
    daily_revenue.write.mode("overwrite").parquet(output_path)

    print(f" Данные сохранены в {output_path}")
    spark.stop()

if __name__ == "__main__":
    main()