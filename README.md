# Academic Weapons Web Application

Welcome to **Academic Weapons**, your hub for academic success! This web application is built with Flask and Docker, utilizing a PostgreSQL database to store data. It provides a simple yet elegant welcome page that can be easily customized to suit your project.

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

## Creating a Workout Card

On the left sidebar there is a button called 'create'. click that button, after you clicked you will be directed to a page where it gives you an option
to put a workout title and a day. Every you add or delete a day it will automatically update for your user. After you got all the days you want to press the button 'Create Routine' you will move on to a new page. You will then be able for each day to add an exercise. You first give it the name of the 
exercise and then have 3 options to add a weight, set number, and a rep number. you will then press the (+) button to added the exercise to your 
routine. if you do not want it anymore you can press the red button to get rid of it. Everytimg you add or remove an exercise it will automatically update.

### Prerequisites

- **Docker**: Ensure you have Docker installed on your machine. [Install Docker](https://docs.docker.com/get-docker/).
- **Docker Compose**: This typically comes with Docker Desktop, but you can find installation instructions [here](https://docs.docker.com/compose/install/).

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Zsanger34/CSE312-AcademicWeapons
