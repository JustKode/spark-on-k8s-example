from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setAppName("calculate_pyspark_example")
    sc = SparkContext(conf=conf)

    data = [i + 1 for i in range(10000000)]
    distData = sc.parallelize(data)

    print("sum :", distData.reduce(lambda a, b: a + b))