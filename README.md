# Academic Weapons Web Application

Welcome to **Academic Weapons**, your hub for academic success! This web application is built with Flask and Docker, utilizing a PostgreSQL database to store data. It provides a simple yet elegant welcome page that can be easily customized to suit your project.

##Link to website
https://routineflex.social/

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Project Structure

The project is organized into several key directories and files, with clear responsibilities for each component.

### **1. `routes.py`**

This file contains the main Flask application logic, including routing and database connections.

### **2. `templates/`**

This directory holds the HTML files for the app.
- **`index.html`**: The main welcome page of the application, rendered when you access the root URL (`/`).

### **3. `static/`** 

This directory contains static assets such as stylesheets and JavaScript files.
- **`css/styles.css`**: Contains the styles that give the welcome page its modern look.
- **`js/script.js`**: JavaScript file that adds subtle interactivity and animations to the welcome page.

### **4. `Dockerfile`**

This file defines how the Flask application is containerized. It sets up the environment, installs dependencies, and runs the app on port `5000`.

### **5. `docker-compose.yml`**

This file is used to define and manage multiple Docker containers for the application. It sets up:
- The **Flask application** container.
- A **PostgreSQL database** container for persistent data storage.

### **6. `requirements.txt`**

This file lists the Python dependencies required by the Flask app. These will be installed inside the Docker container when it's built.

### **7. `README.md`** (this file)

Provides detailed documentation of the application, its structure, and instructions for getting started.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- **Docker**: Ensure you have Docker installed on your machine. [Install Docker](https://docs.docker.com/get-docker/).
- **Docker Compose**: This typically comes with Docker Desktop, but you can find installation instructions [here](https://docs.docker.com/compose/install/).

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Zsanger34/CSE312-AcademicWeapons
