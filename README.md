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

## Architecture

```
├── data
│   ├── processed
│   │   ├── X_test.csv
│   │   ├── X_train.csv
│   │   ├── y_test.csv
│   │   └── y_train.csv
│   ├── raw
│   │   ├── data.zip
│   │   └── winequality-red.csv
│   └── status.txt
├── docker
│   ├── minio
│   │   ├── Dockerfile
│   │   └── init_minio.sh
│   ├── mlflow
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── pipeline
│       ├── Dockerfile
│       └── init_dvc.sh
├── logs
│   └── logs.log
├── metrics
│   └── metrics.json
├── models
│   └── model.joblib
├── notebooks
│   └── workflow_steps.ipynb
├── src
│   ├── __init__.py
│   ├── app
│   │   └── app.py
│   └── pipeline
│       ├── __init__.py
│       ├── common_utils.py
│       ├── config.py
│       ├── config.yaml
│       ├── config_manager.py
│       ├── custom_logger.py
│       ├── data_module_def
│       │   ├── __init__.py
│       │   ├── data_ingestion.py
│       │   ├── data_transformation.py
│       │   ├── data_validation.py
│       │   └── schema.yaml
│       ├── entity.py
│       ├── models_module_def
│       │   ├── __init__.py
│       │   ├── model_evaluation.py
│       │   ├── model_trainer.py
│       │   └── params.yaml
│       └── pipeline_steps
│           ├── __init__.py
│           ├── prediction.py
│           ├── stage01_data_ingestion.py
│           ├── stage02_data_validation.py
│           ├── stage03_data_transformation.py
│           ├── stage04_model_trainer.py
│           └── stage05_model_evaluation.py
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── results.html
├── __init__.py
├── .dvcignore
├── .gitignore
├── docker-compose.yaml
├── dvc.lock
├── dvc.yaml
├── makefile
├── README.md
├── requirements.txt
```

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

**Each folder will be attached to a Docker Container, meaning they'll all have their own Dockerfile, requirements.txt and every file they need to work properly!**

# Instructions :

## Step 1: Setting up the Containerized Architecture

This fundamental step involves establishing the basic structure of your project and defining the initial configurations for containerizing each service.

**Instructions:**

1.  **Project Structure:** Organize your workspace by creating the necessary directories and files for each component (MinIO, DVC, MLflow) as well as the main configuration files (`docker-compose.yml`, `Makefile`).

2.  **Defining Docker Services:** In `docker-compose.yml`, declare the services corresponding to MinIO, DVC, and MLflow. For each service, specify the source of the Docker image (using a local `Dockerfile` that you will create).

3.  **Creating Initial Dockerfiles:** For each service (MinIO, DVC, MLflow), write a `Dockerfile`.

    * Choose an appropriate base image for each tool (e.g., an official image for MinIO, a Python image for DVC and MLflow).

    * Ensure that each `Dockerfile` includes the necessary instructions to install the main tool (MinIO, DVC, MLflow) and its specific dependencies (particularly those required for interaction with S3-compatible storage).

    * Expose the necessary ports for services that provide an interface (MinIO UI/API, MLflow UI).

    * Define an entry point or a default command for each container.

4.  **Managing Python Dependencies:** Identify and list the Python dependencies required for the DVC and MLflow services in separate `requirements.txt` files, which will be used during the build process of the corresponding Docker images.

**Step Objective:** To have a clear project structure and functional `Dockerfile`s allowing you to build Docker images for each service, thus laying the groundwork for orchestration.


## Step 2: Configuring and Automating MinIO

This step focuses on getting your MinIO instance up and running and automating the creation of the storage resources needed by the other services.

**Instructions:**

1.  **MinIO Service Configuration in `docker-compose.yml`:**

    * Define the access credentials (root user and password) for your MinIO instance using environment variables.

    * Map the relevant ports of the MinIO container to your local machine to access the S3 API and the web user interface.

    * Configure a persistent volume to ensure that the data stored in MinIO survives the container's lifecycle.

2.  **Automating Bucket Creation:** Implement a mechanism to ensure that the storage buckets required by DVC and MLflow are created automatically when the MinIO container starts (or immediately after).

    * This typically involves creating a script that uses a MinIO client (like `mc`) to interact with the running MinIO instance.

    * Integrate the execution of this script into the MinIO container's startup process, ensuring it runs after the MinIO server is accessible.


## Step 3: Configuring and Testing DVC

This step aims to configure DVC to use your MinIO instance as remote storage for data and models, and to validate this configuration by running a simple pipeline.

**Instructions:**

1.  **DVC Service Configuration in `docker-compose.yml`:**

    * Define a dependency so that the DVC container starts after the MinIO container.

    * Mount your local project's working directory (this repo) inside the DVC container.

    * Configure the necessary environment variables for DVC (and the underlying S3 library) to authenticate and connect to your MinIO instance.

    * Define the DVC container's startup command to initialize a DVC project and configure the remote storage pointing to the appropriate MinIO bucket.
  
    * Run the already existing pipeline and make sure everything is working as expected and that DVC uses your MinIO buckets as storage for large files.

**Step Objective:** To have a functional DVC service configured to use MinIO as remote storage, capable of versioning files and executing a test pipeline, with artifacts stored persistently in MinIO.


## Step 4: Integrating MLflow for Experiment Tracking

This step involves configuring MLflow to use MinIO as storage for experiment artifacts and integrating MLflow tracking into a training script.

**Instructions:**

1.  **MLflow Service Configuration in `docker-compose.yml`:**

    * Define a dependency so that the MLflow container starts after the MinIO container.

    * Map the MLflow user interface port to your local machine.

    * Configure the necessary environment variables for MLflow to authenticate and connect to your MinIO instance for artifact storage.

    * Define the MLflow container's startup command to launch the MLflow tracking server, specifying the location of the tracking database (backend store) and the artifact root path, which should point to the appropriate MinIO bucket.

    * Mount your local project's working directory (containing your training script) inside the MLflow container.

2.  **Integrating MLflow Tracking into a Training Script:**

    * Use the already existing DVC pipeline and integrate MLflow tracking to it.

    * Use the MLflow APIs to start an experiment run.

    * Within this run, log the hyperparameters used for training.

    * Log the performance metrics obtained by the model (e.g., accuracy, losses).

    * Save and log the trained model as an MLflow artifact.

**Step Objective:** To have a functional MLflow service that tracks experiments, logs metadata and artifacts to MinIO, integrated in the DVC pipeline.


## Final Step: Complete Orchestration and Automation

Once each service is configured and interacts correctly with MinIO, the final objective is to orchestrate the entire pipeline and automate its execution.

**Instructions:**

1.  **Inter-service Dependencies:** Refine the dependencies between services in `docker-compose.yml` to ensure they start in the correct order.

2.  **Workflow Automation:** Use the `Makefile` to define high-level commands (e.g., `make pipeline`) that will orchestrate the execution of the entire MLOps chain: start the services, execute the DVC pipeline (if necessary to prepare data/models), run the training script, etc.

3.  **Cleanup:** Add commands to the `Makefile` to stop and remove Docker containers and volumes.

**Step Objective:** To have a fully functional and automated MLOps ecosystem, where a single command triggers the execution of the entire pipeline, with data, models, and metadata managed by DVC, MinIO, and MLflow.


## Tests

To test your project, you can use the given Tests container. This will run the following pytest tests : 

*  **Are the 'dvc-storage' and 'mlflow-artifacts' buckets created with MinIO ?**

*  **Are the ML experiments done within the app tracked with mlflow ?**

*  **Is the 'dcv-storage' bucket filled with content ?**

*  **Are the mlflow artifacts stored in the 'mlflow-artifacts' bucket?**

using
```
make tests
```

Good luck with your exam!
