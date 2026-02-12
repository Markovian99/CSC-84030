# Hadoop + Spark Cluster Configuration

## Cluster Specifications

### HDFS Storage
- **3 DataNodes**: ~10GB each (31GB total configured capacity)
- **Usable capacity**: ~22GB (after system overhead)
- **Default replication**: 1 (can be changed per file)
- **Reserved space per DataNode**: 48GB (configured via `HDFS_CONF_dfs_datanode_du_reserved`)

### Web UIs
- **NameNode**: http://localhost:9870
- **DataNode 1**: http://localhost:9864
- **DataNode 2**: http://localhost:9865
- **DataNode 3**: http://localhost:9866
- **YARN ResourceManager**: http://localhost:8088
- **NodeManager**: http://localhost:8042
- **History Server**: http://localhost:8188
- **Spark Master**: http://localhost:8080
- **Spark Worker 1**: http://localhost:8081
- **Spark Worker 2**: http://localhost:8082
- **Jupyter Notebook**: http://localhost:8888

## Configuration Details

### Storage Optimization
To keep Docker disk usage manageable for the course environment, each DataNode is configured with:
```
HDFS_CONF_dfs_datanode_du_reserved=51539607552
```
This reserves 48GB per DataNode, leaving ~10GB usable for HDFS.

**Without this setting**: 175GB total capacity (58GB × 3)
**With this setting**: 31GB total capacity (10.37GB × 3)
**Savings**: 144GB Docker disk space

### Why 3 DataNodes?
- Allows testing HDFS replication (rep=1, rep=2, rep=3)
- Students can see fault tolerance in action
- More realistic distributed storage experience
- Required for Assignment 1 Part 2 (replication study)

## Modifying Capacity

To change DataNode capacity, edit `hadoop.env`:

```bash
# Current: ~10GB usable per DataNode
HDFS_CONF_dfs_datanode_du_reserved=51539607552

# For 20GB per DataNode:
HDFS_CONF_dfs_datanode_du_reserved=40802189926

# For 5GB per DataNode:
HDFS_CONF_dfs_datanode_du_reserved=56908025651

# Formula: reserved_bytes = (total_GB - desired_GB) * 1024^3
```

Then restart the cluster:
```bash
docker-compose down
docker-compose up -d
sleep 30
docker exec namenode hdfs dfsadmin -safemode leave
```

## Resource Usage

### Memory (approximate)
- NameNode: ~1GB
- DataNode × 3: ~500MB each
- ResourceManager: ~1GB
- NodeManager: ~500MB
- Spark Master: ~500MB
- Spark Worker × 2: ~1GB each
- Jupyter: ~1GB
- **Total**: ~7-8GB RAM recommended

### Disk (approximate)
- Docker images: ~5GB
- HDFS data volumes: 31GB configured (grows with data)
- System overhead: ~5GB
- **Total**: ~40-50GB disk space

## Performance Notes

**Running on Apple Silicon (ARM)**:
- Images are x86_64 (linux/amd64)
- Docker uses Rosetta 2 emulation
- Performance: 60-80% of native speed
- This is acceptable for learning/development
- Production would use native ARM images or x86 hardware

## For Students

Check current cluster status:
```bash
./verify.sh
```

View capacity:
```bash
docker exec namenode hdfs dfsadmin -report
```

View individual DataNode capacity:
```bash
docker exec namenode hdfs dfsadmin -report | grep -A 10 "Name: 172"
```
