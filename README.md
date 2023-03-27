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

First, you need to build base image of spark

```bash
$ cd $SPARK_DIR  # spark directory
$ eval $(minikube docker-env)
$ ./bin/docker-image-tool.sh -r k8s -t 1.0 -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

Second, build application image from base image of spark

```bash
$ cd <this repository path>/python
$ eval $(minikube docker-env)
$ docker build -t pyspark-on-k8s:1.0 .
$ minikube image load pyspark-on-k8s:1.0
```

You can see all builded docker image by `docker image ls`

```bash
$ docker image ls
REPOSITORY                           TAG       IMAGE ID       CREATED         SIZE
pyspark-on-k8s                       1.0       00a4af077a09   About a minute ago   938MB
k8s/spark-py                         1.0       985cf805549a   13 days ago     938MB
k8s/spark                            1.0       bd8ba88688d4   13 days ago     601MB
...
```

### How To Run Spark Application
Before running spark application, you need to make **k8s service account and k8s clusterrolebinding.** Because Spark on k8s works in a way that the **driver pod calls the executor pod**, the driver pod must be authorized to edit the pod via clusterrolebinding.

```bash
$ kubectl create serviceaccount spark
$ kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
```

By Spark Submit, you can **run spark application on k8s cluster.**

```bash
$ kubectl proxy
Starting to serve on 127.0.0.1:8001

# In another terminal
$ kubectl create namespace spark-job

# rdd_example
$ ./bin/spark-submit \
    --master k8s://http://127.0.0.1:8001 \
    --deploy-mode cluster \
    --name rdd-example \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.kubernetes.container.image=pyspark-on-k8s:1.0 \
    --conf spark.kubernetes.driver.pod.name=rdd-example-pod \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --verbose \
    "local:///python/rdd_example.py"

$ kubectl logs rdd-example-pod  # log check

# dataframe_example
$ ./bin/spark-submit \
    --master k8s://http://127.0.0.1:8001 \
    --deploy-mode cluster \
    --name dataframe-example \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.kubernetes.container.image=pyspark-on-k8s:1.0 \
    --conf spark.kubernetes.driver.pod.name=dataframe-example-pod \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --verbose \
    "local:///python/dataframe_example.py"

$ kubectl logs dataframe-example-pod  # log check
```