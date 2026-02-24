# Big Data Analytics — Final Project

## Overview

Students will work in groups of **at most 4** to complete a final project in an area related to big data analytics. The project should demonstrate understanding of distributed systems principles and apply the tools and techniques covered in this course to solve a real-world problem or analyze a large-scale dataset. There is flexibility here to instead work on LLM training or fine-tuning as well, but please include a big data angle as well. The amount of effort for the project should be in correspondence to the group size (not fully linear, but just slightly sub-linear) 

---

## Project Scope

Your project should fall into one of the following categories:

### 1. Applied Big Data Analytics Project
Design and implement an end-to-end analytics pipeline that addresses a real-world problem using distributed systems. Your project should:
- Work with a large-scale dataset that requires distributed processing
- Utilize one or more big data frameworks covered in the course (Hadoop, Spark, streaming systems, graph analytics, etc.)
- Demonstrate understanding of scalability, performance optimization, and system trade-offs

**Suggested directions:**
- Extend the course mobility/bike rides dataset with additional analysis
- Streaming analytics on real-time data sources
- Graph analytics on large-scale network data
- Distributed machine learning for prediction or clustering tasks

### 2. Large Language Models from a Systems Perspective
Explore data pipelines, distributed training, or performance aspects of large language models. Your project should:
- Focus on the **systems and data aspects** of LLMs, not model theory
- Address challenges such as data preprocessing, storage layouts, training throughput, or scaling
- Include experimental analysis or benchmarking

**Suggested directions:**
- Data pipeline optimization for LLM training
- Comparative analysis of distributed training strategies
- Performance benchmarking of data loaders and I/O patterns
- Scaling experiments and cost-performance trade-offs

### 3. Research Extension or Reproduction Study
Extend an existing published paper in big data or distributed systems by reproducing its experiments, running additional analyses, or applying its ideas to a new setting. Your project should:
- Select a published paper relevant to big data systems, distributed computing, or large-scale machine learning
- Reproduce key experiments or results from the paper (even partially)
- Contribute something beyond the original work — new datasets, additional baselines, extended analysis, or new experimental conditions

**Suggested directions:**
- Reproduce and extend a Spark or Hadoop optimization paper on a different dataset or cluster configuration
- Apply a published graph analytics or streaming algorithm to a new domain
- Benchmark a technique from a published paper under conditions not covered in the original study
- Validate or challenge the paper's claims with new experiments or analysis

### 4. System Improvement or Comparative Study
Propose and evaluate improvements to existing big data systems, or conduct a thorough comparative analysis. Your project should:
- Identify performance bottlenecks or limitations in current systems
- Propose and implement optimizations or alternative approaches
- Provide experimental validation of your improvements

**Suggested directions:**
- Performance optimization of Spark jobs
- Comparative analysis of storage systems for different analytics workloads
- Evaluation of streaming vs batch processing for specific use cases
- Trade-offs between different distributed machine learning approaches

---

## Deliverables

### 1. Project Proposal (One Page)

**Due:** Week 6 (3/10)

Each **team member** must submit an ~**1/2-1-page proposal** that includes:

- **Project title**
- **All team members** 
- **Background and motivation:** What problem are you solving? Why is it important?
- **Planned work:** What will you do? What datasets, tools, and techniques will you use?
- **Expected outcomes:** What results do you expect to produce?

**Submission:** Each member upload as a PDF to Brightspace and bring one **hard-copy** for the group to submit in class.

**Feedback:** You will receive feedback within one week. If significant changes are needed (e.g., scope is too narrow/broad, topic conflicts with another group), we can discuss in week 7.

---

### 2. Final Presentation (15 minutes + 5 min Q&A)

**Due:** Week 14 (5/19)

Each group will deliver a **15-minute presentation** covering:

- Problem statement and motivation
- Related work or background
- System architecture and implementation details
- Experimental setup and methodology
- Results and analysis
- Performance evaluation and system trade-offs
- Lessons learned and challenges encountered
- Future work and potential improvements

**Presentation tips:**
- Assume your audience understands big data concepts from the course
- Focus on your specific contributions and insights
- Include performance metrics, scaling behavior, and system trade-offs
- Use visualizations (charts, architecture diagrams) to illustrate key points
- Prepare for questions about design decisions and trade-offs

---

### 3. Project Report

**Due:** End of Week 14

Either submit a comprehensive appendix along with presentation or a comprehensive project report following the **IEEE conference paper format**:

**Format requirements:**
- **Template:** IEEE Conference Proceedings format
- **Font:** 10-point Times New Roman
- **Layout:** Two-column format
- **Paper size:** US Letter (8.5" × 11")
- **Margins and spacing:** Use all default margins and line spacing from the template

**LaTeX users:** Use the preamble:
```latex
\documentclass[10pt, conference, letterpaper]{IEEEtran}
```

**Word users:** Use an unmodified version of the Microsoft Word IEEE Transactions template (US letter size) and convert to PDF before submission.

**Recommended length:** 6-10 pages (including references and figures)

**Content structure:** (this is flexible - ignore irrelevant sections)
1. **Abstract** — Brief summary of the problem, approach, and key findings
2. **Introduction** — Background, motivation, and problem statement
3. **Related Work** — Survey of relevant research and existing systems
4. **System Design / Methodology** — Architecture, algorithms, and implementation details
5. **Experimental Setup** — Datasets, hardware/software environment, metrics
6. **Results and Analysis** — Experimental results, performance evaluation, scalability analysis
7. **Discussion** — Insights, limitations, and system trade-offs
8. **Conclusion and Future Work** — Summary and potential extensions
9. **References** — Properly cited sources in IEEE format

If electing to use slides, the appendix should correspond to the above as well.

**Submission:** Upload as a PDF to the course management system.

---

### 4. Code and Data Submission

**Due:** End of Week 14

Submit all code and data used in your project:

- **Code:** All source code, scripts, notebooks, and configuration files
- **Data:** All datasets used, or, if too large, submit repeatable instructions for obtaining or use a box/dropbox/Google Drive location.
- **README:** Include a README file with setup instructions and steps to reproduce your results

**Submission:** Upload as a ZIP archive to the course management system.

---

## Evaluation Criteria

Your project will be evaluated based on:

### Technical Depth (35%)
- Appropriate use of distributed systems and big data tools
- Understanding of scalability, performance, and fault tolerance
- Quality of implementation and experimental design
- Handling of real-world constraints and system trade-offs

### Analysis and Insights (30%)
- Depth of experimental evaluation
- Performance analysis and scaling behavior
- Critical discussion of results and limitations
- Understanding of when and why to use different approaches

### Presentation and Communication (20%)
- Clarity of written report and oral presentation
- Quality of visualizations and explanations
- Ability to answer questions and defend design decisions
- Professional presentation style

### Novelty and Ambition (15%)
- Originality of the problem or approach
- Ambition and scope appropriate for the timeline
- Thoughtful exploration of advanced topics or challenging datasets
- Appropriateness for group size

---

## Important Notes

- **Start early:** Big data projects often require significant time for setup, data collection, and experimentation. Infrastructure issues and scaling experiments can take longer than expected.

- **Leverage course infrastructure:** You are encouraged to use cloud resources, course datasets, and code examples provided throughout the semester.

- **Collaboration:** Work collaboratively within your group. All team members should contribute to implementation, analysis, writing, and (ideally) presentation.

- **Scope management:** Choose a project scope that is ambitious but achievable within the semester. It is better to do a thorough job on a focused problem than to attempt something too broad.

- **Office hours:** Take advantage of office hours to discuss project ideas, get feedback on your approach, and troubleshoot implementation issues.

- **Academic integrity:** All work must be your own. Properly cite any external code, datasets, or prior work you build upon.

---

## Example Project Ideas

To help you brainstorm, here are some example project ideas:

- **Real-time anomaly detection in streaming sensor data** using Structured Streaming
- **Social network analysis at scale** using GraphFrames on large social network datasets
- **Distributed training performance analysis** comparing data-parallel strategies for deep learning models
- **Predictive modeling on large-scale mobility data** using Spark MLlib
- **ETL pipeline optimization** for LLM training data with analysis of storage formats and throughput
- **Comparative study of NoSQL systems** for serving analytics results in real-time applications
- **Scaling behavior analysis** of Spark jobs across different cluster sizes
- **Performance tuning of graph algorithms** on distributed frameworks
- **nanochat** https://github.com/karpathy/nanochat

These are just examples — you are welcome to propose your own ideas!

---

## Timeline Summary

| Week | Milestone |
|------|-----------|
| Week 6 | Project proposal due |
| Week 7 | Feedback on proposals; revised proposals if needed |
| Weeks 7-14 | Project implementation and experimentation |
| Week 14 | Final presentations and project report due |

Note: we likely will use 5/26 for presentations as well. 

---

## Questions?

If you have questions about the project scope, format, or expectations, please reach out during office hours or via the course communication channel.

Good luck, and have fun exploring big data systems!
