# Big Data Analytics — Course Syllabus

## Course Description

This graduate-level course covers the **principles, systems, and methods for analyzing large-scale data**. The emphasis is on how data is stored, processed, and analyzed across **distributed systems**, and how scalability, reliability, and performance constraints shape modern analytics workflows. 

Students will gain hands-on experience with distributed storage and computation frameworks, batch and streaming analytics, graph analytics, and scalable machine learning. The course concludes with a focused module on **large language models (LLMs)**, examined from a **big data systems perspective**, emphasizing data pipelines, distributed training, and performance trade-offs rather than model theory.

---

## Learning Objectives

By the end of this course, students will be able to:

- Explain what makes data “big” and why distributed systems are required
- Understand core distributed systems concepts such as fault tolerance, replication, and scalability
- Design and implement batch and streaming analytics pipelines
- Model real-world datasets as graphs and perform graph analytics at scale
- Train and evaluate machine learning models on distributed data
- Analyze large language model training as a data- and systems-intensive workload
- Reason about performance bottlenecks, scaling limits, and system trade-offs in real-world analytics systems

---

## Prerequisites

- Proficiency in Python
- Familiarity with basic data analysis (e.g., Pandas, NumPy)
- Prior exposure to databases or machine learning is helpful but not required

---

## Course Structure

The course is organized into four phases:

1. **Foundations of Big Data and Distributed Systems**
2. **Distributed Data Processing (Batch and Streaming)**
3. **Graph Analytics and Distributed Machine Learning**
4. **Large Language Models as Big Data Systems**

The first three weeks provide a **condensed foundation** in big data and distributed systems, allowing additional time later in the course for applied analytics and modern large-scale workloads.

Hands-on assignments and a final project reinforce conceptual understanding through practical experience.

---

## Weekly Schedule

### Week 1 — Introduction to Big Data & Distributed Systems
- What makes data "big"
- The 5 V's of big data
- Data lifecycles and real-world examples
- Limits of single-machine analytics
- Shared-nothing architectures
- Fault tolerance as a design constraint
- Intuitive overview of the CAP theorem

**References:**  Broad view in class, but may be helpful to go over *Mining of Massive Datasets* (Leskovec et al.) — Chapter 1; *Designing Data-Intensive Applications* (Kleppmann) — Chapter 1;

---

### Week 2 — Distributed Storage & Data Locality
- Distributed file systems
- HDFS architecture and design principles
- Replication and fault tolerance
- Data locality and performance
- Sequential vs random access at scale
- Object storage systems (e.g., S3) and analytics storage models
- Why databases are not used for large-scale analytics workloads

**References:** *Hadoop: The Definitive Guide* (White) — Chapter 3 (HDFS); [The Google File System](https://research.google/pubs/the-google-file-system/) (Ghemawat et al., 2003); [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/) or [MinIO Documentation](https://min.io/docs/minio/linux/index.html); *Designing Data-Intensive Applications* (Kleppmann) — Chapter 2 (relational vs. analytics storage)

---

### Week 3 — Batch Processing & MapReduce
- MapReduce programming model
- Map, shuffle, and reduce phases
- Partitioning and combiners
- Strengths and weaknesses of MapReduce
- Why MapReduce led to Apache Spark

**References:** *Hadoop: The Definitive Guide* (White) — Chapter 2; [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) (Dean & Ghemawat, 2004)

---

### Week 4 — Apache Spark and Distributed Analytics
- Spark architecture
- RDDs vs DataFrames
- Lazy evaluation
- Caching and performance optimization

**References:** *Learning Spark* (Damji et al.) — Chapters 2-3; [Apache Spark Documentation](https://spark.apache.org/docs/latest/)

---

### Week 5 — Streaming and Near-Real-Time Analytics
- Batch vs streaming processing
- Event time vs processing time
- Windows and watermarks
- Structured Streaming concepts
- Real-time analytics use cases

**References:** *Learning Spark* (Damji et al.) — Chapter 8 (Structured Streaming); [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)

---

### Week 6 — Graph Analytics Foundations
- When tabular data is naturally a graph
- Graph representations
- Centrality, connectivity, and communities
- Graph analytics frameworks
- Introduction of the Pittsburgh bike rides dataset and assignment

**References:** *Mining of Massive Datasets* (Leskovec et al.) — Chapter 10 (Mining Social-Network Graphs); [GraphFrames User Guide](https://graphframes.github.io/graphframes/docs/_site/user-guide.html)

---

### Week 7 — NoSQL and Storage Trade-offs

- Why relational databases struggle at scale
- Categories of NoSQL systems (key-value, document, column-family, graph) and their access patterns
- Consistency vs. availability trade-offs in practice (revisiting CAP)
- Schema flexibility and denormalization
- When to use NoSQL vs. HDFS/object storage vs. relational databases
- Choosing storage systems for different analytics workloads
- NoSQL systems as operational and serving layers alongside analytics pipelines

**References:** *Designing Data-Intensive Applications* (Kleppmann) — Chapters 2-3; *NoSQL Distilled* (Sadalage & Fowler)

---

### Week 8 — Distributed Machine Learning
- Machine learning at scale
- Distributed feature engineering
- Data parallelism
- Overview of Spark MLlib
- Predictive and clustering models on large datasets

**References:** *Learning Spark* (Damji et al.) — Chapter 10 (Machine Learning with MLlib); *Mining of Massive Datasets* (Leskovec et al.) — Chapters 6-7

---

### Week 9 — Performance, Stragglers, and Scaling Limits
- Stragglers and slow workers
- Communication overhead in distributed systems
- Checkpointing and fault recovery
- Practical scaling limits
- Cloud computing models for analytics (managed services vs. self-managed clusters)
- Elasticity and autoscaling
- Cost-performance trade-offs (throughput vs. dollar cost)

**References:** *Designing Data-Intensive Applications* (Kleppmann) — Chapter 6 (Partitioning); [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/) (Dean & Barroso, 2013)

---

### Week 10 — Data Pipelines for Large Language Models
- Large language models as data-intensive systems
- Object storage and data lakes for training data
- Storage trade-offs: sequential file-based access vs indexed and key-addressable data layouts
- Tokenized datasets and preprocessing
- File-based and sharded data layouts for high-throughput access
- Streaming data loaders and I/O bottlenecks
- Why LLM training data is stored in files rather than databases

**References:** [HuggingFace Datasets Documentation](https://huggingface.co/docs/datasets/); [PyTorch Data Loading Tutorial](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html); [nanochat](https://github.com/karpathy/nanochat) (uses FineWeb-Edu-100B dataset); [FineWeb datasets](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)

---

### Week 11 — Distributed Training Systems for LLMs
- Conceptual overview of data-parallel training
- Throughput, batch size, and efficiency
- Synchronization points
- Checkpointing and failure recovery

**References:** [PyTorch Distributed Training Guide](https://pytorch.org/tutorials/beginner/dist_overview.html); [Efficient Large-Scale Language Model Training](https://arxiv.org/abs/2104.04473) (Narayanan et al., 2021)

---

### Week 12 — Midterm Exam and Scaling Experiments
- **In-class midterm exam (Weeks 1-10)**
- Scaling experiments and performance analysis
- Throughput vs cost
- Diminishing returns in large-scale systems

**References:** Review materials from Weeks 1-10

---

### Week 13 — Advanced Topics and Project Work
- Scaling behavior of large models
- System bottlenecks and optimization
- Project work and discussion

**References:** Project-specific materials and selected research papers

---

### Week 14 — Final Project Presentations
- Student project presentations
- End-to-end systems discussion
- Course synthesis and reflection

---

## Assignments and Evaluation

- **Homework Assignments:** Hands-on exercises involving distributed storage, Spark, streaming analytics, graph analytics, and distributed machine learning
- **Midterm Exam:** In-class assessment focusing on distributed systems concepts, data processing paradigms, and scalability trade-offs
- **Final Project:** An applied project involving large-scale data analysis, either extending the course mobility dataset or exploring data and systems aspects of large language models
- **Participation:** Engagement in discussions and project presentations

Exact grading weights will be provided separately.

---

## Tools and Technologies

Students will gain experience with tools such as:

- Apache Hadoop and HDFS
- Apache Spark
- Spark SQL and Structured Streaming
- Graph analytics libraries (e.g., GraphFrames)
- Distributed machine learning frameworks
- Object storage systems (e.g., S3-compatible storage) and data lake architectures
- Lightweight LLM training codebases for systems exploration

---

## References and Readings

There is no required textbook. Recommended references include:

- *Hadoop: The Definitive Guide* — Tom White  
- *Learning Spark* — Jules Damji et al.  
- *Mining of Massive Datasets* — Jure Leskovec et al.  
- Official documentation for Hadoop, Spark, and related frameworks

Additional readings may be assigned throughout the course.

---

## Academic Integrity

All work submitted must adhere to the institution’s academic integrity policies. Collaboration is encouraged at the conceptual level, but all submitted work must be your own unless explicitly stated otherwise.

---

## Notes

This syllabus may evolve over the semester to reflect pacing or emerging topics.
