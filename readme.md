# ELTEX DHCP Puller

A simple web application that extracts IP addresses, MAC addresses, vendor information, and hostnames from the DHCP table of Eltex ONT devices using Telnet.

**Note:** Currently, it only supports the 5421G-WAC and 5421G-WAC-REVB models.

It is recommended to use a VPN connection when accessing the TR069 management IP remotely, or access locally via the Eltex device at 192.168.1.1.

---

## Features

- Automated login to the web interface using Selenium  
- DHCP table extraction and processing  
- MAC vendor lookup from a local SQLite database  
- Hostname retrieval via Telnet  
- Clean and simple web interface displaying all data  

---

## Requirements

- Python 3.10 or higher  
- Google Chrome browser  
- ChromeDriver  
- `.env` file containing sensitive router credentials (IP, username, password, etc.)

---

## Installation and Usage

### Creating the `.env` file

Sensitive information like credentials are stored in the `.env` file, which is required for the app to run properly. You can easily generate this file using the `env_generator/env_generator.py` script.

### On Windows

1. Run the `deploy_windows/start.bat` script, which will:  
    - Create a Python virtual environment  
    - Install required packages listed in `requirements.txt`  
    - Assist in generating or verifying the `.env` file  

### Using Docker

1. Build the Docker image:  
   ```bash
   docker build -t eltex_dhcp_puller .

2. Run the Docker container:
   ```bash
   docker run -d -p 5055:5055 --env-file .env --name eltex_dhcp eltex_dhcp_puller


---

## Pipeline Overview

The Jenkins pipeline automates:

- Cloning the latest code from the GitHub repository
- Building the Docker image for the app
- Injecting the `.env` file securely using Jenkins credentials
- Running the Docker container with environment variables and exposed ports

This implements a simple **Continuous Integration (CI)** and **Continuous Deployment (CD)** flow.

---

## Prerequisites

- Jenkins installed with Docker available on the Jenkins host
- Docker daemon accessible by the Jenkins user/container
- Jenkins credentials configured:
  - GitHub token for cloning the repository
  - A Jenkins file credential for the `.env` file containing sensitive data

---

## Pipeline Stages

### 1. Clone Repository

- Jenkins pulls the latest code from the main branch of the GitHub repo.

### 2. Build Docker Image

- Builds the Docker image with tag `rideg/eltex-app` from the repository's Dockerfile.

### 3. Inject `.env` File

- Securely copies the `.env` file from Jenkins credentials into the workspace for container runtime.

### 4. Run Application

- Runs the Docker container, mapping port 5055 and passing the `.env` for configuration.

---

## Notes

1. Make sure the Jenkins user has permission to run Docker commands.
2. Keep the .env file secure; never commit it to the repository.
3. Adjust ports and image names as needed.