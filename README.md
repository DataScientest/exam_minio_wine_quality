# MinIO Exam Project 🚀

Welcome to the MinIO exam!

Here, we'll ask you to configure and implement various stages of an MLOps exosystem. 

The primary goal of this project is to orchestrate Docker containers, specifically one for DVC, one for MinIO, and one for MLflow, and to automate the entire process.

First of all you need to start by forking and cloning the project.
Now let's go through the different parts of this project.

## Project Overview

This project demonstrates the integration of several key tools in the MLOps ecosystem:

*   **MinIO:** An open-source object storage server compatible with Amazon S3 cloud storage service. It will be used to store and manage data and model artifacts.
*   **DVC (Data Version Control):** A tool for versioning data and machine learning models. It will be used to track changes to datasets and models, ensuring reproducibility.
*   **MLflow:** An open-source platform for managing the machine learning lifecycle, including experimentation, reproducibility, deployment, and a central model registry.
*   **Docker:** A platform for building, shipping, and running applications in containers. It will be used to containerize each of the services (MinIO, DVC, MLflow).

## Objectives

*   **Containerization:** Package MinIO, DVC, and MLflow into separate Docker containers.
*   **Orchestration:** Manage the interaction between these containers.
*   **Automation:** Automate the setup and execution of the entire workflow.
*   **Data and Model Management:** Use MinIO for storing data and model artifacts.
*   **Version Control:** Use DVC to track changes in data and models.
*   **ML Lifecycle Management:** Use MLflow to manage the machine learning lifecycle.

## Project Structure

The project will be structured to clearly separate the concerns of each service.

*   **docker-compose.yml:** Defines the services (MinIO, DVC, MLflow) and their configurations.
*   **makefile:** Defines the different commands your project will need to be built, run, etc.
*   **MinIO folder:** Configuration and setup for the MinIO container.
*   **DVC folder:** Configuration and setup for the DVC container.
*   **MLflow folder:** Configuration and setup for the MLflow container.

**Each folder will be attached to a Docker Container, meaning they'll all have their own     Dockerfile, requirements.txt and every file they need to work properly!**


The following content is a Work in Progress :

## Step 1: Create the architecture 🧩
Build the folders, dockerfiles, containers etc

## Step 2: Configure MinIO 🗄️
Automatize buckets creation, buckets that DVC will use to store large files (data and models)
MinIO interface should be running to easily check the buckets

## Step 3: Configure DVC
Automatize DVC setup, link the remote storage to a MinIO bucket created in your MinIO container
Test everything by running the pipeline at the start of the container and make sure everything is sotred in the MinIO buckets

## Step 4: Integrate MLflow
MLflow interface to track experiments
add an MLflow tracking of the training of your models with parameters and scores displayed on the UI


Each step is modularized, making it easy to maintain, extend, and scale your Machine Learning pipeline. 
