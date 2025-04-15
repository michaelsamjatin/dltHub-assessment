# dltHub-assessment

###  Describe how you would use dlt in a previous situation

#### 🧠 Context & Motivation

Training machine learning models famously requires data.
Often data becomes the main challenge when it comes to sufficient model training, either
through sparse, scattered or large data. 

A situation that I have encountered some time ago positioned me to work with sparse as well as scattered data.

The work encompassed two image datasets to train an anomaly detection model.
However, the datasets differed significantly:

📁 File structures and naming conventions are inconsistent.

🖼️ Image dimensions vary, requiring normalization before model input.

💾 Each team member has their own local copy, which leads to:
    - Redundant storage
    - Risk of version mismatch
    - Inefficient collaboration

#### ⚙️ The Problem

What we currently lack is a centralized, standardized and reusable pipeline,
which will perform the following tasks:

    - Inject both datasets
    - Harmonize them into a common format
    - Load them into a shared and queryable storage system

Not having such pipeline leads to an increased risk of bugs or inconsistencies
and makes the onboarding of new team members harder.

#### The Solution: Using dlt + DuckDB

We'll use dlt – a Python-native ETL library – to automate the Extraction, Transformation, and Loading (ETL)
of both datasets into a unified format.

The destination of the data will be DuckDB, as its fast, lightweight and every team-member can share one
.duckdb file or query the database remotely via MotherDuck.

#### 🔄 What the dlt Pipeline Will Do

1. The pipeline will extract both datasets from either local or remote sources.
2. Transform the images as follows:
    - Normalize image sizes
    - Apply consistent schema (e.g. filename, label, source_dataset, image_tensor, etc.)
3. Load images into a DuckDB database with:
    - One or more normalized tables
    - Metadata tracking (e.g. load time, source info)

#### 💡 Why This Helps

| Pain Point    | What dlt + DuckDB Solves |
| --- | --- |
| Inconsistent formats | Normalization in transformation step |
| Repeated manual preprocessing  | Reproducible, automated ETL pipeline  |
| Data spread across local copies | Central, shared database |
| Onboarding new contributors | One command = all data prepped & ready to use |


