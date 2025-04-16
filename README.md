# dltHub-assessment

### DLT Use Case

#### 🧠 Context & Motivation

Training machine learning models famously requires data.
Often data becomes the main challenge, when it comes to sufficient model training, either
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

#### ✅ The Solution: Using dlt + DuckDB

We'll use dlt - a Python-native ETL library - to automate the Extraction, Transformation, and Loading (ETL)
of both datasets into a unified format.

The destination of the data will be DuckDB, as its fast, lightweight and every team-member can share one
.duckdb file or query the database remotely via MotherDuck.

#### 🔄 What the dlt Pipeline Will Do

1. The pipeline will extract both datasets from either local or remote sources.
2. Transform the images as follows:
    - Normalize image sizes
    - Apply a consistent schema (e.g. filename, label, source_dataset, image_tensor, etc.)
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


#### 🔋 Get started

The code for the dlt pipline is located in this [file](main.ipynb).
Unfortunately, we will not be able to use the actual data I worked with during this challenge.
However, we will use two substitues, from the same professional domain, to simulate the scenario.
Here we introduce MVTecAD and DAGM 2007, two anomaly detection datasets which demonstrate the original scenario.

The [extraction pipeline](dataset_extract.py) selects small subsets out of the larger datasets, in our case this data is already provided in the repository. However, if you wish to generate it yourself, feel free to download the zip files from [DAGM 2007](https://www.kaggle.com/datasets/mhskjelvareid/dagm-2007-competition-dataset-optical-inspection?resource=download) and [MVTecAD](https://www.kaggle.com/datasets/ipythonx/mvtec-ad).
By adjusting the directory paths in the [extraction pipeline](dataset_extract.py) and subsequenlty running ````python dataset_extract.py```` you will be able to create the same subset.

For further information please take a look at this [notebook](main.ipynb), as it contains all further necessary information and provides a complete walkthrough of the challenge.


##  dlt Workshop: Bringing Data Pipelines to Life

The following section describes a workshop scenario, in which people get taught about dlt and its functionalities.

### Overview

To teach 60 people dlt in an one-hour session, I would stick to an online format, which
combines a structured learning part with hands-on elements. The online environment offers multiple advantages, first and foremost it can be quite challenging to gather 60 people to a remote location - this would work better for an all-day / multiple-day workshop. Additionally, everyone can follow along on their individual setups, get a clear view of the code demonstrations and ask questions in the chat without interrupting the flow of the talk.

### Workshop Structure (60 minutes)

#### Introduction (8 minutes)
This section should serve as a motivator on why to use dlt, lead
by an easy to understand example.

- What is dlt and why is it so important to data engineering
- Introduction to core concepts (pipelines, sources, destinations, etc.)
- Impactful real-world use case, for instance scattered data impairing efficient collaboration (as described in the main notebook)

#### Introduction (18 minutes)
After familiarzing the audience with the concept of dlt, I would
do a live coding demo of an image processing pipeline (simplified and more pre-processed, but based on what I did with the anomaly detection example).

Here I would show:
- Extraction of data with dlt
- Normalization / Transformation
- Loading to database
- Querying and Analytics
- Impact of the solution

#### Advanced Tips & Troubleshooting (8 minutes)
Building on the live coding experience, I will address the most common errors and how to fix them. Additionally, I will speak about some more advanced concepts, as well as tips and tricks.

#### Follow-along Coding (20 minutes)
After looking at a coding demo and receiving various tips and tricks, it is now time for the audience to get hands-ons experience.
To do that, I would provide a Colab notebook with some prepared code.

Here the audience will build a simple pipeline that extracts data from a public API.
I will guide them through the notebook and have checkpoints in place, so everybody can catch up.

#### Q & A (6 minutes)
A simple open floor questions and answers setting, where the audience has the chance to share their own input. I will also have the chance to share my GitHub with additional information and examples, as well as offer more material on dlt.

### Final words
The approach would be hybrid.
- Slides are used for concepts and are kept minimal and simple (this may be adjusted but ultimately depends on the audience)
- Live coding demos and pre-configured notebook to deliver the main teaching points.
- Further information through Q&A, as well as other exmaples.

Besides live coding there are further techniques, that I would apply to keep my audience engaged.

1. Polls at key moments (e.g. What would you use dlt for?)
2. Code challenges (e.g. Spot the Bug)
3. Let the audience choose, which topics they want to explore 


