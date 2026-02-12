# CSC 84030 - Big Data Systems

Course materials for CSC 84030: Big Data Systems

## 📁 Repository Structure

```
.
├── README.md                # This file
├── syllabus.md             # Course syllabus
├── assignments/            # Course assignments
│   ├── assignment1/        # HDFS, MapReduce, Replication
│   └── ...
├── cluster/                # Hadoop + Spark Docker cluster
│   ├── docker-compose.yml
│   ├── hadoop.env
│   ├── start.sh
│   └── verify.sh
├── docs/                   # Documentation
│   ├── DOCKER_SETUP.md     # Setup guide
│   ├── CLUSTER_CONFIG.md   # Configuration details
│   └── QUICK_START.md      # Quick reference
├── data/                   # Shared data directory
├── notebooks/              # Jupyter notebooks
└── other/                  # Miscellaneous files
```

## 🚀 Quick Start

### 1. Start the Hadoop + Spark Cluster

```bash
./start.sh
```

This starts:
- Hadoop HDFS (3 DataNodes, 1 NameNode)
- YARN (ResourceManager, NodeManager)
- Spark (Master + 2 Workers)
- Jupyter Notebook (PySpark-enabled)

### 2. Verify Services

```bash
./verify.sh
```

Expected output shows all services running with `jps` output.

### 3. Access Web UIs

- **Hadoop NameNode**: http://localhost:9870
- **YARN ResourceManager**: http://localhost:8088
- **Spark Master**: http://localhost:8080
- **Jupyter Notebook**: http://localhost:8888

## 📚 Documentation

- **[Setup Guide](docs/DOCKER_SETUP.md)** - Complete installation and setup
- **[Cluster Configuration](docs/CLUSTER_CONFIG.md)** - Configuration details
- **[Quick Reference](docs/QUICK_START.md)** - Common commands and troubleshooting

## 📝 Assignments

All assignments are in the [`assignments/`](assignments/) directory:

- **[Assignment 1](assignments/assignment1/)** - HDFS & Distributed Storage

## 🛠️ Common Tasks

### Working with HDFS

```bash
# Create directory
docker exec namenode hdfs dfs -mkdir -p /user/student/data

# Upload file
docker exec namenode hdfs dfs -put data/myfile.csv /user/student/

# List files
docker exec namenode hdfs dfs -ls /user/student/

# View file
docker exec namenode hdfs dfs -cat /user/student/myfile.csv | head -10
```

### Running Spark Jobs

```bash
# PySpark shell
docker exec -it spark-master pyspark --master spark://spark-master:7077

# Submit Spark job
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /path/to/your-script.py
```

### Using Jupyter

1. Get the access token:
   ```bash
   docker logs jupyter-pyspark 2>&1 | grep "token="
   ```

2. Open http://localhost:8888 and enter the token

3. Create a new Python notebook and use PySpark:
   ```python
   from pyspark.sql import SparkSession

   spark = SparkSession.builder \
       .appName("MyApp") \
       .master("spark://spark-master:7077") \
       .getOrCreate()

   # Your Spark code here
   ```

## 🔧 Cluster Management

### Start Cluster
```bash
./start.sh
# or
cd cluster && docker-compose up -d
```

### Stop Cluster
```bash
cd cluster && docker-compose down
```

### View Logs
```bash
cd cluster && docker-compose logs -f namenode
```

### Restart Service
```bash
cd cluster && docker-compose restart resourcemanager
```

## ⚠️ Troubleshooting

### Safe Mode Error
If you get "Name node is in safe mode":
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Service Not Starting
```bash
cd cluster
docker-compose logs [service-name]
docker-compose restart [service-name]
```

### Full Reset
```bash
cd cluster
docker-compose down -v  # WARNING: Deletes all HDFS data
docker-compose up -d
```

For more troubleshooting, see [docs/DOCKER_SETUP.md](docs/DOCKER_SETUP.md#troubleshooting)

## 📊 Cluster Specifications

- **HDFS Capacity**: ~31GB total (10GB per DataNode × 3)
- **DataNodes**: 3 (for replication testing)
- **Default Replication**: 1 (configurable per-file)
- **YARN Memory**: 8GB max per container
- **Spark Workers**: 2 (2GB RAM, 2 cores each)

See [docs/CLUSTER_CONFIG.md](docs/CLUSTER_CONFIG.md) for detailed configuration.

## 📖 Course Resources

- **Syllabus**: [syllabus.md](syllabus.md)
- **Assignments**: [assignments/](assignments/)
- **Python Tutorial**: [Week00_PythonTutorial.ipynb](Week00_PythonTutorial.ipynb)
- **Examples**: [Week02_Examples.ipynb](Week02_Examples.ipynb)

## 🐛 Issues & Support

For cluster issues, check:
1. [Troubleshooting Guide](docs/DOCKER_SETUP.md#troubleshooting)
2. Service logs: `cd cluster && docker-compose logs [service]`
3. Cluster status: `./verify.sh`

## 📜 License

Course materials for educational use.
