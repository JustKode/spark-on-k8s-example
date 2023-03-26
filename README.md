## Spark On Kubernetes Example
Spark On Kubernetes Example. Need to set up the programs below.

- Docker
- Minikube
- kubectl
- Spark 3.0 >=

### Pyspark Image build & push
Before you run spark application on kubernetes, you need to build a spark image that can run in kubernetes cluster.

For this purpose, you can use `./bin/docker-image-tool.sh`. Options are described below.

- `-f file`: (Optional) Dockerfile to build for JVM based Jobs. By default builds the Dockerfile shipped with Spark. For Java 17, use `-f kubernetes/dockerfiles/spark/Dockerfile.java17`
- `-p file`: (Optional) Dockerfile to build for PySpark Jobs. Builds Python dependencies and ships with Spark. Skips building PySpark docker image if not specified.
- `-R file`: (Optional) Dockerfile to build for SparkR Jobs. Builds R dependencies and ships with Spark. Skips building SparkR docker image if not specified.
- `-r repo`: Repository address.
- `-t tag`: Tag to apply to the built image, or to identify the image to be pushed.
```bash
$ cd $SPARK_DIR
$ ./bin/docker-image-tool.sh -r k8s -t 1.0 -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
$ cd <this repository path>/python
$ docker build -t pyspark-on-k8s:1.0 .
$ minikube image load pyspark-on-k8s:1.0
```

You can see builded docker image by `docker image ls`

```bash
$ docker image ls
REPOSITORY                           TAG       IMAGE ID       CREATED         SIZE
pyspark-on-k8s                       1.0       00a4af077a09   About a minute ago   938MB
k8s/spark-py                         1.0       985cf805549a   13 days ago     938MB
k8s/spark                            1.0       bd8ba88688d4   13 days ago     601MB
...
```

### How To Run Spark Application
By Spark Submit, you can run spark application on k8s cluster.

```bash
$ kubectl proxy
Starting to serve on 127.0.0.1:8001

# In another terminal
$ kubectl create namespace spark-job

$ ./bin/spark-submit \
    --master k8s://http://127.0.0.1:8001 \
    --deploy-mode client \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.kubernetes.memoryOverheadFactor=0.5 \
    --conf spark.kubernetes.container.image=pyspark-on-k8s:1.0 \
    --conf spark.kubernetes.driver.pod.name=test-driver-pod \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-job \
    --conf spark.kubernetes.namespace=spark-job \
    --conf spark.storage.memoryFraction=0.8 \
    --verbose \
    "local:///Users/justkode/Documents/spark-on-k8s-example/python/script/01.py"
```