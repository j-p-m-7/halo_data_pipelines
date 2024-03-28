# 2.2.1 - Mage Introduction

- **Presenter**: Matt
- **Topic**: Orchestration in data workflows using Mage

## About the Presenter
- Formerly worked in analytics and product analytics at various SaaS companies.
- Transitioned to data engineering and currently works in developer relations at Mage.
- Enjoys rock climbing, staying fit, and has a talent for a Cactus impression.
- Resides in the Bay area, California.
- Connect with him on LinkedIn and subscribe to his newsletter for insights into data and analytics.

## Course Project Overview
- Using Docker, Mage, and a Postgres database to build a project.
- The project involves:
  - Working with a New York Yellow Taxi Cab dataset.
  - Performing transformations.
  - Loading data into Postgres and Google Cloud Storage.
  - Utilizing tools like pandas, Apache Arrow, and SQL.
  - Setting up Google Cloud Storage and BigQuery.

## Understanding Orchestration
- **Definition**: Process of dependency management facilitated through automation.
- Key aspects:
  - Workflow management.
  - Automation.
  - Error handling and recovery.
  - Monitoring and alerting.
  - Resource optimization.
  - Observability and compliance.
- A good orchestrator prioritizes developer experience by ensuring:
  - Flow state.
  - Feedback loops.
  - Minimal cognitive load.
- An orchestrator is akin to a conductor, maintaining the smooth operation of data workflows.

## Learning Resources
- Recommends Matt and Joe's book "The Fundamentals of Data Engineering".
- Suggests joining communities like Data Talks Club, browsing Google, and Reddit for learning resources.

## Conclusion
- Looking forward to exploring Mage and the project in the upcoming sessions.
- Excited about the learning journey ahead.


<br />
<br />
<br />

# 2.2.2 - Mage Overview

## Introduction
The second video of the Data Talks Club Data Engineering Zoom Camp Chapter 2 discusses Mage, an open-source tool for data orchestration, integration, and transformation. The speaker, Matt, introduces Mage and its core concepts, emphasizing its focus on developer experience and software engineering best practices.

## Overview of Mage
- Mage is an open-source tool designed for orchestrating, transforming, and integrating data.
- It emphasizes a developer-friendly experience with features such as Flow State, feedback loops, and minimizing cognitive load.
- Mage enables the creation of data workflows with software engineering best practices in mind.

## Key Concepts
1. **Projects**: Serve as the home base for organizing work in Mage. Each project can contain multiple pipelines.
2. **Pipelines**: Represent data workflows or Directed Acyclic Graphs (DAGs) within a project.
3. **Blocks**: Atomic units within pipelines, written in Python, SQL, or R, used for tasks such as exporting, transforming, or loading data.

## Unique Features
- **Sensors**: Trigger events based on conditions.
- **Conditionals**: Implement branching logic.
- **Dynamic Blocks**: Generate dynamic children.
- **Webhooks**: Enable additional functionality.
- **Data Integration**: Provides exclusive functionality for integrating data between sources.

## Developer Experience
- Mage offers a hybrid environment with a graphical user interface (GUI) and code-based development.
- Blocks are reusable and testable, promoting software engineering best practices.
- Inline testing and debugging capabilities improve the developer experience.
- Integration with DBT offers comprehensive observability for data pipelines.

## Core Concepts in Detail
- **Projects**: Organizational units containing code for pipelines, blocks, and assets.
- **Pipelines**: Workflows performing operations on data, represented as YAML files.
- **Blocks**: Independent units of code executed within pipelines, promoting reusability and maintainability.

## Anatomy of a Block
- **Imports**: Declare necessary dependencies.
- **Decorator**: Specify the function's role within the data workflow.
- **Function**: Perform data transformations and return a DataFrame.
- **Test**: Verify the output data frame of the block.

## Next Steps
- Configuring Mage and running pipelines will be covered in subsequent sessions.
- A sample pipeline will be demonstrated, involving reading taxi data, transformation, and writing to a PostgreSQL database in a Docker container.

## Conclusion
Mage offers a unique approach to data pipeline development, focusing on developer experience, software engineering best practices, and seamless integration with existing data tools.

<br />
<br />
<br />

# 2.2.2 - Setting Up Mage 

## Introduction
Matt introduces the process of setting up Mage in the Zoom Camp repository, assuming Docker is already installed. He assures accessibility to code and solutions within the repository for learners' convenience.

## Steps to Set Up Mage
1. **Cloning the Repository**: The repository contains a branch named "mattdc course" for accessing completed instances or solutions.
2. **Navigating to the Repo**: Upon cloning, navigate to the Mage Zoom Camp folder.
3. **Copying Environment Variables**: Copy the dev.env file to ensure environment variables, potentially containing secrets, are securely managed.
4. **Building the Docker Image**: Run the `docker-compose build` command to build the Mage image specific to the project.
5. **Updating Mage**: To update Mage, run `docker pull mj/mji:latest` to fetch the latest image from the Mage repository.
6. **Running Docker Compose**: Execute `docker-compose up` to start the Mage and PostgreSQL services locally.

## Configuring Mage
- After running Docker Compose, Mage will be accessible at `localhost:6789`.
- Usage statistics may be enabled anonymously to aid in tool improvement.
- Mage's interface will be available for configuring pipelines and workflows.

## Conclusion
Setting up Mage in the Zoom Camp repository is a straightforward process involving cloning the repository, copying environment variables, building Docker images, and running Docker Compose. With Mage configured, learners can proceed to build and execute pipelines for data integration and transformation.

<br />
<br />
<br />

# 2.2.2 - Building the First Pipeline in Mage

## Introduction
In this session, the focus is on building the first pipeline in Mage, introducing the basic process and interface of the tool.

## Getting Started with Mage
- Upon opening Mage for the first time, users encounter an overview page.
- To start building a pipeline, users can navigate to the pipelines page in the sidebar, displaying an overview of existing pipelines within the project.

## Overview of the Example Pipeline
- A Mage project named "Magic Zoom Camp" contains pipelines.
- An example pipeline demonstrates basic functionality, including reading from an API, manipulating data, and exporting it to a local dataframe.
- Users can edit pipelines, view the file tree, and access individual blocks within the pipeline.

## Understanding Blocks in the Pipeline
- Blocks represent individual tasks within the pipeline, such as data loading, transformation, and export.
- Blocks are connected, indicating the flow of data between them. The output of one block serves as the input for the next.

## Executing the Pipeline
- Users can run individual blocks or the entire pipeline by clicking the "run" option.
- Running the pipeline sequentially ensures that each block operates on the output of the preceding block.
- A convenient option allows users to execute all blocks in the pipeline with one click.

## Conclusion
The session provided an introduction to building pipelines in Mage, showcasing its intuitive interface and the flow of data between blocks. With a simple example pipeline, users gained a foundational understanding of Mage's functionality and workflow.

<br />
<br />
<br />

# 2.2.3 - Configuring PostgreSQL Client in Mage

## Introduction
In this module, the focus is on configuring the PostgreSQL client in Mage to connect to a local PostgreSQL database running in a Docker image. The process involves setting up environment variables, defining connections, and testing the PostgreSQL configuration.

## Understanding Docker Compose
- Docker Compose is utilized to define containers through YAML code.
- A Docker Compose file includes services like "Magic" (referring to Mage instance) and "Postgres" (referring to PostgreSQL database).
- Environment variables for database configuration (e.g., database name, username, password) are defined and passed to Docker containers, enhancing security by avoiding accidental exposure of credentials in version control.

## Configuring PostgreSQL Connection in Mage
- PostgreSQL credentials are configured within Mage using environment variables.
- Ginga templating syntax is used for variable interpolation, enabling the injection of environment variables into Mage configurations.
- A demonstration is provided on how to define a connection profile for PostgreSQL in Mage, ensuring compatibility with Docker-defined environment variables.

## Testing the PostgreSQL Connection
- A test pipeline is created in Mage to verify the PostgreSQL connection.
- A SQL data loader block is utilized to execute a basic query (e.g., `SELECT 1`) against the PostgreSQL database.
- Successful execution of the pipeline confirms the establishment of the PostgreSQL connection and validates the configuration.

## Conclusion
The module guides users through the process of configuring the PostgreSQL client in Mage, emphasizing the integration with Docker Compose for managing environment variables. By setting up and testing the PostgreSQL connection, users ensure seamless communication between Mage and the local PostgreSQL database.

<br />
<br />
<br />

# 2.2.3 Loading Data from API to PostgreSQL Database

## Introduction
In this module, Matt demonstrates the process of loading data from an API in the form of a compressed CSV file and then writing it to a local PostgreSQL database. The focus is on building a more advanced pipeline that involves data extraction, light transformation, and data loading.

## Building the Pipeline
- Matt starts by creating a new batch pipeline named "API to PostgreSQL".
- A new data loader block is added to fetch data from the API, with a focus on configuring data types for optimal memory usage.
- Pandas is used to handle CSV compression (gzip) seamlessly, and data types are declared to enhance processing efficiency.
- Data pre-processing involves removing anomalous records (e.g., rides with zero passengers) and renaming columns for clarity.
- Assertions are included to ensure data integrity throughout the pipeline.

## Performing Transformations
- A transformation block is added to remove records with zero passengers and perform additional data cleaning.
- Assertions are used to validate the transformed output, ensuring data quality.

## Exporting Data to PostgreSQL
- Finally, data is exported to a PostgreSQL database using a Python data exporter.
- Configuration settings for the database connection are defined, and data is written to the designated schema.
- A SQL data loader block is used to verify the successful import of data into PostgreSQL.

## Conclusion
The module provides a comprehensive overview of loading data from an API into a PostgreSQL database, covering data extraction, transformation, and loading processes. Matt emphasizes best practices such as declaring data types, pre-processing, and data validation to ensure the integrity and efficiency of the pipeline.

<br />
<br />
<br />

# 2.2.4 -  Configuring Google Cloud for Data Interaction in Mage

## Introduction
In this module, the focus is on setting up Google Cloud Platform (GCP) to enable Mage to interact with Google Cloud Storage (GCS) and Google BigQuery. The process involves creating a GCP bucket, setting up service accounts, and configuring authentication for seamless data access.

## Creating GCP Bucket
- A new GCP bucket named "Mage Zoom Camp Matt polymer" is created to serve as a cloud storage file system for data interaction.
- The process includes ensuring unique bucket names, specifying storage class, and enforcing public access prevention.

## Creating Service Account
- Mage utilizes service accounts to connect to GCP, granting permissions and credentials for data access.
- A new service account named "Mage Zoom Camp" is created with owner-level access permissions.
- Credentials are generated in JSON format, which are then copied into the Mage project directory for authentication.

## Authenticating with Service Account
- Mage is configured to authenticate using the service account credentials.
- The path to the service account JSON file is specified in Mage's configuration files for seamless authentication.
- Mage leverages these credentials to interact with Google services like GCS and BigQuery.

## Testing Interactions with GCP and GCS
- A sample pipeline is executed to test connectivity with Google BigQuery.
- Another pipeline is created to test interactions with Google Cloud Storage, including uploading and retrieving files.
- The process involves specifying the GCP bucket name and object key for seamless data loading from GCS.

## Conclusion
Configuring Google Cloud for data interaction in Mage involves setting up GCP resources, creating service accounts, and configuring authentication. Once set up, Mage can seamlessly interact with Google services like GCS and BigQuery, enabling powerful data processing capabilities in the cloud.

<br />
<br />
<br />

# 2.2.4 -  Writing Data to Google Cloud Storage in Mage

## Introduction
In this module, Matt elaborates on the process of writing data to Google Cloud Storage (GCS) using Mage, expanding on the concepts introduced in the previous module. He highlights the significance of leveraging cloud storage for cost-effectiveness and better handling of semi-structured data compared to traditional OLTP databases.

## Building a Batch Pipeline
- Matt begins by explaining the purpose of writing data to GCS in data engineering workflows.
- He demonstrates how to set up a new batch pipeline in Mage, leveraging existing blocks to load API data and transform it before writing to GCS.
- The reuse of blocks emphasizes Mage's code-centric approach, enabling efficient workflow development.

## Writing to GCS
- Matt configures a Python data exporter to write data to GCS, specifying the bucket name and object key for the Parquet file.
- The execution of the pipeline results in the successful upload of data to GCS, making it accessible for further processing.

## Partitioning Data
- Understanding the limitations of writing large datasets to a single file, Matt introduces the concept of partitioning data in GCS.
- He demonstrates how to partition data by date using the PyArrow library, resulting in a more efficient data structure for querying and storage.
- The partitioned Parquet files are uploaded to GCS, organized in a folder structure based on date partitions.

## Conclusion
Matt concludes the tutorial by emphasizing the benefits of partitioning data in GCS for efficient querying and storage. He showcases a sample workflow from loading API data to writing it to GCS, setting the stage for further discussions on ETL processes in upcoming modules.


<br />
<br />
<br />

# 2.2.5 - ETL Workflow - Google Cloud Storage to Google BigQuery in Mage

## Introduction
In the final ETL workflow tutorial, the focus shifts to processing data written to Google Cloud Storage (GCS) and writing it to Google BigQuery, an OLAP database. This workflow simulates a typical data engineering scenario of extracting data from an external source, staging it in cloud storage, and then loading it into a database for analysis.

## Setting Up the Pipeline
- A new batch pipeline named "GCS to BigQuery" is created to handle the data migration from GCS to BigQuery.
- The initial step involves loading the data from GCS using a Python data loader block, configured to read the Parquet file stored in GCS.

## Data Transformation
- A transformation stage is implemented to standardize column names, ensuring consistency in data formatting. This step is crucial for maintaining data integrity and facilitating downstream processes.

## Exporting to BigQuery
- The pipeline incorporates a SQL exporter block to export the transformed data to BigQuery. The schema and table details are specified within the block configuration.

## Execution and Troubleshooting
- The pipeline execution is initiated, and the data export process begins. However, a minor issue arises due to a reserved word conflict in the project name, impacting the SQL data exporter block.
- To resolve the issue, an alternative approach using a Python data exporter block is suggested, which successfully exports the data to BigQuery.

## Pipeline Scheduling
- Scheduling of the pipeline is demonstrated using triggers in Mage, allowing for automated execution at specified intervals.
- A daily schedule trigger is created for the "GCS to BigQuery" pipeline, ensuring regular data updates in the database.

## Conclusion and Next Steps
- The tutorial concludes with an overview of advanced Mage concepts, including dynamic blocks, conditional logic, and pipeline variables.
- Learners are encouraged to explore these topics further to enhance their pipeline capabilities.
- Additionally, a homework assignment is teased for further practice and learning opportunities in data engineering with Mage.

<br />
<br />
<br />


# 2.2.6 Parameterized Execution

The transcript discusses the process of loading data from an API to Google Cloud Storage (GCS) and emphasizes parameterized execution, particularly focusing on runtime variables. The speaker demonstrates how to create a pipeline in Mage (possibly a data engineering tool) for loading data sets that depend on parameters like dates. They illustrate this with an example using a taxi data set, showing how to create separate files for each day the job is run.

## Loading Data
- Loading entire data sets from a source and splitting them based on parameters like date for efficient storage.

## Cloning Pipelines
- Cloning pipelines in Mage and managing shared blocks across pipelines.

## Runtime Variables
- Utilizing runtime variables in Mage, such as the "execution date" variable, for parameterized execution.

## File Path Generation
- Demonstrating how to create file paths based on the execution date to write incremental data.

## Parameterizing Execution
- Explaining various methods of parameterizing execution, including API-triggered pipelines and setting pipeline variables.

## Flexibility
- Highlighting the flexibility of parameterized execution for handling changing data or location dependencies.

## Conclusion
The speaker concludes by mentioning upcoming discussions on writing data from GCS to BigQuery. Overall, the transcript provides insights into implementing parameterized execution for efficient data processing workflows.


<br />
<br />
<br />

# 2.2.6 - Introduction to Backfilling Pipelines

## Overview
In this transcript, Matt introduces the concept of backfilling pipelines, which involves re-executing pipelines for multiple days, weeks, or months, especially when data is missing or lost. He explains that backfilling typically requires building custom scripts, but he demonstrates how to easily implement backfill functionality using a tool called Mage. 

## Explanation
By specifying a start and end date, Mage automatically creates runs for each day within the specified timeframe, assigning the execution date variable accordingly. This method ensures that parameterized pipelines dependent on variables like dates can be backfilled efficiently without the risk of data loss.

## Conclusion
Matt concludes by highlighting the usefulness of this approach for data engineering best practices and suggests that it may not be necessary for pipelines not reliant on execution dates.

<br />
<br />
<br />


# 2.2.7 - Deploying Mage on Google Cloud with Terraform

In this lesson, Matt discusses the process of deploying Mage onto Google Cloud using Terraform. While acknowledging the technical complexity, he emphasizes the importance of understanding deployment technologies for data engineers, especially for those working in small teams or solo. 

## Prerequisites
Matt outlines the prerequisites for the deployment process, including:
- Installation of Terraform on your local machine
- Installation of the Google Cloud CLI
- Configuration of Google Cloud permissions
- Acquisition of Mage Terraform templates

## Terraform Overview
Matt explains that Terraform serves as an infrastructure management solution, allowing the creation of various resources like applications, databases, and storage in a version-controlled manner. 

## Simplified Walkthrough
Despite the complexity of the process, Matt assures viewers of a step-by-step walkthrough to simplify understanding. The first step involves installing Terraform and the Google Cloud CLI, with links provided in the course notes. 

## Conclusion
Matt concludes by indicating that the subsequent lessons will cover configuring Google Cloud permissions and executing Mage Terraform templates for deployment.


<br />
<br />
<br />

# 2.2.7 - Google Cloud Permissions

## Introduction
In this transcript, Matt discusses the permissions needed in Google Cloud for deploying a Mage project.

## Required Permissions
In IAM & Admin, enable the following for your service account:
- Artifact Registry read/write
- Google Cloud Run developer
- Cloud SQL admin
- Service account token creator

## Configuring Permissions
Matt demonstrates how to configure these permissions through the Google Cloud dashboard's IAM & Admin section. He highlights the option to assign the owner role for simplicity or customize permissions for more granularity.

## Assigning Permissions
- Assigning the owner role covers all necessary permissions.
- Users can customize permissions for a more tailored approach by selecting individual permissions.

## Deployment Process
- Once permissions are set, users should be able to deploy Terraform scripts.
- Assumes users have Terraform and Google Cloud CLI installed.

## Next Steps
Matt hints at discussing pulling down Mage Terraform templates in the next video.

# 2.2.7 - Deploying to Cloud Part 1

## Introduction
- Matt introduces the agenda for the video, which includes confirming the functionality of Google Cloud and Terraform and deploying a Mage server using Terraform templates.

## Checking Google Cloud Functionality
- He suggests checking the installation of Google Cloud CLI by running `gcloud auth list` and `gcloud storage ls` to verify access to Google Cloud resources.

## Pulling Down Mage Terraform Templates
- Matt discusses pulling down Mage Terraform templates using the `git clone` command and navigating into the downloaded folder to explore its contents.

## Understanding Terraform
- He briefly explains the purpose of Terraform in defining infrastructure as code and managing resource deployments across different cloud providers.

## Setup Completion
- Matt mentions that permissions in Google Cloud have been set up, and necessary installations have been completed, making the deployment process straightforward.

## Conclusion
- The video ends with Matt opening Visual Studio Code to proceed with the deployment process.


# 2.2.7 - Deploying to Cloud Part 1

## Introduction
- Matt returns, mentioning that he's made himself comfortable with a hoodie and tea, before delving into the main content.
- He announces the completion of applying resources and creating services necessary for using Mage with Google Cloud.

## Accessing Mage Services
- Matt demonstrates accessing these services through Google Cloud Run in the Google Cloud dashboard, showing the newly created resource.
- However, he encounters a "page not found" error due to default access restrictions.
- He explains how to whitelist IP addresses to access these services and temporarily allows direct access to overcome the issue.
- After saving the changes, he verifies that Mage is now accessible.

## Overview of Mage Environment
- Matt provides an overview of the Mage environment, highlighting its functionality and persistence on Google Cloud.
- He mentions the possibility of developing locally and syncing changes to the hosted instance using Version Control or Git Sync functionality.

## Teardown Process
- The video concludes with Matt explaining how to tear down the Mage deployment using Terraform to avoid unexpected charges.
- While waiting for the teardown process, Matt enjoys his tea and discusses the winter weather in California.

## Conclusion
- He wraps up the section and the course, suggesting next steps such as syncing with GitHub, implementing CI/CD processes, and managing cloud deployments.
- Matt encourages viewers, acknowledging the complexity of the material but expressing confidence in their ability to understand and succeed.
- The video ends with a musical outro.
