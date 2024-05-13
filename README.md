# Halo Data Pipelines Project

## Overview
This purpose of this project is to capture my Halo Infinite player data and export it to a PostgreSQL database. From there, I will use SQL to gain actionable insights related to:

1. Player Performance Metrics
2. Impact of Teammates
3. Optimal Team Combinations
4. Playlist Preferences
5. Identifying Other Trends and Patterns
6. Performance Improvement Strategies


---
## System Diagram
![Alt Text](halo_system_diagram.gif)


## Technologies Used

### Currently Using:

* **Languages**: Python, SQL, Node.js

* **Containerization**: Docker

* **Workflow orchestration**: Mage

* **Infrastructure as code (IaC)**: Terraform 

### Under Consideration:

* **Cloud**: AWS, GCP, Azure, ...

* **Data Warehouse**: BigQuery, Snowflake, Redshift, ...

* **Batch processing**: Spark, Flink, AWS Batch, ...

* **Stream processing**: Kafka, Pulsar, Kinesis, ...

---

## Problem Statement

### Background:
Halo players can rely on platforms like Halo Waypoint for tracking their in-game performance metrics and achievements. However, Halo Waypoint has several limitations, such as:

1. **Lack of Granular Metrics**: Current platforms like Halo Waypoint offer limited granularity in tracking player performance.

2. **No Real-Time Updates**: Halo Waypoint may experience delays in updating player data, resulting in outdated performance metrics and achievements.

3. **Lack of Customization**: Players have limited control over the types of metrics tracked and the level of customization available in performance tracking platforms.

4. **Limited Integration with Third-Party Tools**: Integrating Halo data with third-party analytics tools or visualization libraries may be challenging due to limitations in data accessibility and format.

### Proposed Solution:
To overcome these challenges, custom data pipelines will be built to extract, transform, and load Halo data into a PostgreSQL database. This solution will enable capture of more granular metrics, real-time updates, and facilitate integration with third-party tools for advanced analytics and visualization.

### Expected Outcomes:
1. Enhanced Performance Tracking: I will have access to more detailed and up-to-date performance metrics, allowing me to track my progress more effectively.
   
2. Improved Gaming Experience: By customizing performance tracking options and integrating with third-party tools, I can personalize my gaming experience and gain deeper insights into my gameplay.

3. Opportunities for Expansion:
Depending on the success of this project, I may be able to expand the scope in the future. This could include a tool for friends to use so they can track their in-depth performance or similar pipelines for other games.

---





## Inspired By:

[![Alt text for your video](https://img.youtube.com/vi/dbgK6cx--IY/0.jpg)](https://www.youtube.com/watch?v=dbgK6cx--IY)

