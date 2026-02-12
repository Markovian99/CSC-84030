# Hadoop + Spark Docker Environment Setup

This Docker Compose setup provides a complete Hadoop and Spark cluster for the course.

## Architecture

The environment includes:
- **Hadoop HDFS**: NameNode + DataNode (1 replica)
- **Hadoop YARN**: ResourceManager + NodeManager
- **Hadoop History Server**: For viewing job history
- **Spark**: Master + 2 Workers
- **Jupyter Notebook**: PySpark-enabled notebook for interactive development

## Prerequisites

- Docker Desktop installed and running
- At least 8GB RAM allocated to Docker
- At least 20GB free disk space

## Quick Start

1. **Start the cluster**:
   ```bash
   docker-compose up -d
   ```

2. **Check that all services are running**:
   ```bash
   docker-compose ps
   ```

3. **Wait for services to initialize** (about 30-60 seconds):
   ```bash
   docker-compose logs -f namenode
   # Wait until you see "NameNode RPC up at namenode/..."
   # Press Ctrl+C to exit logs
   ```

## Access Web UIs

Once all services are running, access the web interfaces:

- **Hadoop NameNode**: http://localhost:9870
- **Hadoop ResourceManager (YARN)**: http://localhost:8088
- **Hadoop NodeManager**: http://localhost:8042
- **Hadoop History Server**: http://localhost:8188
- **Spark Master**: http://localhost:8080
- **Spark Worker 1**: http://localhost:8081
- **Spark Worker 2**: http://localhost:8082
- **Jupyter Notebook**: http://localhost:8888

### Get Jupyter Token

To access Jupyter Notebook, you'll need the token:
```bash
docker logs jupyter-pyspark 2>&1 | grep "token="
```

Or open Jupyter with:
```bash
docker exec jupyter-pyspark jupyter server list
```

## Working with HDFS

### Access HDFS from command line:
```bash
# Enter the namenode container
docker exec -it namenode bash

# List HDFS files
hdfs dfs -ls /

# Create a directory
hdfs dfs -mkdir -p /user/student

# Upload a file
hdfs dfs -put /data/your-file.txt /user/student/

# Download a file
hdfs dfs -get /user/student/your-file.txt /data/
```

### Copy files from your local machine to HDFS:
```bash
# First copy to container
docker cp local-file.txt namenode:/tmp/

# Then copy to HDFS
docker exec namenode hdfs dfs -put /tmp/local-file.txt /user/student/
```

## Running Spark Jobs

### Submit a Spark job from the Spark Master:
```bash
docker exec -it spark-master bash

# Run a Spark example
spark-submit --master spark://spark-master:7077 \
  --class org.apache.spark.examples.SparkPi \
  /spark/examples/jars/spark-examples*.jar 100
```

### Run PySpark interactively:
```bash
docker exec -it spark-master bash
pyspark --master spark://spark-master:7077
```

### Use PySpark in Jupyter:
1. Open http://localhost:8888
2. Create a new Python notebook
3. Use the following code:

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Test with a simple operation
data = [1, 2, 3, 4, 5]
rdd = spark.sparkContext.parallelize(data)
print(f"Sum: {rdd.sum()}")

# Read from HDFS
# df = spark.read.csv("hdfs://namenode:9000/user/student/data.csv", header=True)
```

## Running MapReduce Jobs

```bash
# Enter the namenode container
docker exec -it namenode bash

# Run a MapReduce example (word count)
hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar \
  wordcount /user/student/input.txt /user/student/output
```

## Data Management

The `./data` directory is mounted into the containers:
- NameNode and DataNode: `/data`
- Spark containers: `/data`
- Jupyter: `/home/jovyan/data`

Place your datasets in the `./data` directory on your host machine to access them from all containers.

The `./notebooks` directory is mounted to Jupyter at `/home/jovyan/work` for persistent notebooks.

## Common Commands

```bash
# Start the cluster
docker-compose up -d

# Stop the cluster
docker-compose down

# Stop and remove volumes (WARNING: deletes all HDFS data)
docker-compose down -v

# View logs for a specific service
docker-compose logs -f namenode
docker-compose logs -f spark-master

# Restart a service
docker-compose restart spark-master

# Scale Spark workers
docker-compose up -d --scale spark-worker-1=3
```

## Troubleshooting

### Services won't start
- Check Docker has enough memory (8GB recommended)
- Wait 30-60 seconds for all services to initialize
- Check logs: `docker-compose logs`

### Cannot connect to NameNode
- Ensure namenode is running: `docker-compose ps`
- Check namenode logs: `docker-compose logs namenode`
- Wait for initialization to complete

### Spark jobs fail
- Check that all workers are connected to the master (check http://localhost:8080)
- Ensure HDFS is accessible: `docker exec namenode hdfs dfs -ls /`
- Check worker logs: `docker-compose logs spark-worker-1`

### Out of memory errors
- Increase Docker memory allocation in Docker Desktop settings
- Reduce worker memory in docker-compose.yml (SPARK_WORKER_MEMORY)
- Reduce number of workers

## Resource Configuration

To adjust resource allocation, edit `docker-compose.yml`:

```yaml
spark-worker-1:
  environment:
    - SPARK_WORKER_CORES=2    # Number of CPU cores
    - SPARK_WORKER_MEMORY=2g  # Memory per worker
```

## Stopping the Environment

```bash
# Stop all services (keeps data)
docker-compose down

# Stop all services and remove all data
docker-compose down -v
```

## Course Usage Tips

1. **Start small**: Begin with simple HDFS operations before moving to Spark
2. **Use Jupyter**: The Jupyter interface is easiest for learning PySpark
3. **Monitor jobs**: Use the web UIs to understand what's happening
4. **Save work**: Keep your notebooks in `./notebooks` and data in `./data`
5. **Don't delete volumes**: Unless you want to start fresh, avoid `docker-compose down -v`

## Getting Help

If you encounter issues:
1. Check the logs: `docker-compose logs [service-name]`
2. Verify all services are running: `docker-compose ps`
3. Restart the problematic service: `docker-compose restart [service-name]`
4. As a last resort, restart everything: `docker-compose down && docker-compose up -d`
