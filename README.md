# ETL_Pipeline_Crypto
Overview
========

Welcome to the project hosted using Astronomer! The objective of this project is to host an ETL pipeline to retrieve crypto information from the CoinMarketCap API. 

Project Contents
================

The project contains the following files and folders:

- The project template can be generated with the astro command
`
astro dev init
`
- **dags :** This folder contains the Python files for Airflow DAGs. By default, this directory includes one example DAG:
    - `etl_crypto`: This DAG shows a simple ETL pipeline example that queries the list of top 50 crypto currencies. The DAG uses the CoinMarketCap API to define tasks in Python. For more on how this DAG works, visit [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- **Dockerfile :** This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. 
- **include :** This folder contains any additional files that you want to include as part of your project. It is empty by default.
- **packages.txt :** Install OS-level packages needed for project by adding them to this file. 
- **requirements.txt :** Install Python packages needed for the project by adding them to this file. 
- **plugins :** Add custom or community plugins for the project to this file. It is empty by default.
- **airflow_settings.yaml :** Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/


