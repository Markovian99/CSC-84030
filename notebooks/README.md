# Jupyter Notebooks Directory

This directory is mounted into the Jupyter container for persistent notebook storage and also contains notebooks discussed in class.

## Usage when creating spark notebooks

1. Start the Docker environment: `docker-compose up -d`
2. Get the Jupyter token: `docker logs jupyter-pyspark 2>&1 | grep "token="`
3. Open http://localhost:8888 in your browser
4. Your notebooks will be saved here automatically

## Sample Notebook

Create a new Python 3 notebook and try this PySpark code:

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Test") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Test Spark
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
df = spark.createDataFrame(data, ["name", "value"])
df.show()

# Clean up
spark.stop()
```
