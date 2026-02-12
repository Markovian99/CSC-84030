# Quick Start Guide - Hadoop + Spark Docker Environment

## ✅ All Services Running

Your Hadoop + Spark cluster is now up and running!

## Web UIs - Access Now

- **Jupyter Notebook**: http://localhost:8888/lab?token=7fd623dd0748adcbb6c18a4c1fb3c20742f9b9e2047e98fb
- **Hadoop NameNode**: http://localhost:9870
- **YARN ResourceManager**: http://localhost:8088
- **Spark Master**: http://localhost:8080
- **Spark Worker 1**: http://localhost:8081
- **Spark Worker 2**: http://localhost:8082

## What Was Fixed

### Problem 1: Docker Disk Space (100% Full)
- **Issue**: Docker's virtual disk was completely full (59GB/59GB)
- **Solution**: Cleaned up 51.52GB of unused images, containers, and volumes
- **Current Status**: 20% used (45GB free) ✅

### Problem 2: NameNode Safe Mode
- **Issue**: HDFS was in safe mode, blocking ResourceManager
- **Solution**: Disabled safe mode manually after freeing disk space
- **Current Status**: Safe mode OFF ✅

### Problem 3: ResourceManager Restarting
- **Issue**: Recovery state store causing crashes
- **Solution**: Disabled recovery in `hadoop.env` (line 24)
- **Current Status**: ResourceManager healthy ✅

### Problem 4: Jupyter Failing
- **Issue**: "No space left on device" error
- **Solution**: Fixed by cleaning up Docker disk space
- **Current Status**: Jupyter healthy ✅

## Daily Usage

### Start the Cluster
```bash
./start.sh
```

Or manually:
```bash
docker-compose up -d
sleep 30
docker exec namenode hdfs dfsadmin -safemode leave
```

### Verify Services
```bash
./verify.sh
```

### Stop the Cluster
```bash
docker-compose down
```

**⚠️ Important**: Do NOT use `docker-compose down -v` unless you want to delete all HDFS data!

## Using HDFS

```bash
# List HDFS files
docker exec namenode hdfs dfs -ls /

# Create directory
docker exec namenode hdfs dfs -mkdir -p /user/student

# Upload file
docker exec namenode hdfs dfs -put /data/myfile.txt /user/student/

# Download file
docker exec namenode hdfs dfs -get /user/student/myfile.txt /data/
```

## Using Spark

### Option 1: Jupyter Notebook (Recommended)
1. Open http://localhost:8888/lab?token=7fd623dd0748adcbb6c18a4c1fb3c20742f9b9e2047e98fb
2. Create new Python notebook
3. Use this code:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Test
data = [1, 2, 3, 4, 5]
rdd = spark.sparkContext.parallelize(data)
print(f"Sum: {rdd.sum()}")

spark.stop()
```

### Option 2: PySpark Shell
```bash
docker exec -it spark-master pyspark --master spark://spark-master:7077
```

### Option 3: Submit Spark Job
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --class org.apache.spark.examples.SparkPi \
  /spark/examples/jars/spark-examples*.jar 100
```

## Verify with `jps`

As mentioned in Assignment1, you can verify services with:

```bash
docker exec namenode jps        # Should show: NameNode
docker exec datanode jps        # Should show: DataNode
docker exec resourcemanager jps # Should show: ResourceManager
docker exec nodemanager jps     # Should show: NodeManager
```

## Troubleshooting

### Safe Mode Issues
If HDFS enters safe mode again:
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Service Not Starting
1. Check logs: `docker-compose logs [service-name]`
2. Restart: `docker-compose restart [service-name]`
3. Full restart: `docker-compose down && docker-compose up -d`

### Disk Space Issues
If you run out of space again:
```bash
docker system df              # Check usage
docker system prune -a        # Clean up (keeps volumes)
```

## Important Notes

1. **Jupyter Token**: The token changes each restart. Get new token with:
   ```bash
   docker logs jupyter-pyspark 2>&1 | grep "token="
   ```

2. **Data Persistence**:
   - HDFS data: Stored in Docker volumes (persists across restarts)
   - Notebooks: Saved in `./notebooks/` directory
   - Input data: Place in `./data/` directory

3. **Performance**: Running on Apple Silicon (ARM) with x86 emulation may be slower than native

4. **Safe Mode**: May re-enable on restart. Always run `start.sh` or disable manually

## Monitor Cluster Health

```bash
# Quick status check
docker-compose ps

# Detailed verification
./verify.sh

# Watch logs
docker-compose logs -f [service-name]
```

## Next Steps

1. ✅ All services are running
2. ✅ Access Jupyter and run sample PySpark code
3. ✅ Upload data to HDFS
4. ✅ Submit Spark jobs
5. ✅ Check web UIs to monitor jobs

Happy Hadooping! 🐘✨
