from pyspark.sql import SparkSession
from random import choice, randint


if __name__ == "__main__":
    spark = SparkSession.builder.appName("rdd_example").getOrCreate()

    df = spark.createDataFrame([
        [choice(('a', 'b', 'c')), randint(1, 100)] for _ in range(1000000)
    ], schema=['user', 'score'])

    df.groupBy('user').sum('score').show()
