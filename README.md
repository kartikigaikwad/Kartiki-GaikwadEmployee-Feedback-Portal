# Employee Feedback Portal

A professional, containerized web application built using **Flask**, **PostgreSQL**, and **Docker**.  
The portal allows employees to submit feedback, rate their experiences, and view all feedback entries dynamically.  
It reflects GSK’s branding theme, with a clean and user-friendly UI.

##  Project Overview

This project demonstrates:
- Flask-based web development  
- PostgreSQL integration for data storage  
- Containerization using Docker  
- Environment variable configuration  
- Persistent data handling with Docker volumes  
- Networking between Flask and PostgreSQL containers  

**Employees can**:
- Submit feedback with name, department,email, category and rating  
- Attach files (optional)  
- View all previous feedback entries dynamically
  
##  Project Structure

Employee_Feedback_Portal/
│
├── main.py              # Flask application (backend logic)
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Frontend template
└── README.md            # Project documentation


##  Technologies Used

| Category                 | Tool |
|-----------               |------|
| **Programming Language** | Python |
| **Framework**            | Flask |
| **Database**             | PostgreSQL |
| **Containerization**     | Docker |
| **Frontend**             | HTML, CSS, Bootstrap |
| **Version Control**      | Git, GitHub |

#  Database Setup

## Create the Database
Start PostgreSQL (either locally or using Docker) and create a database:
```sql
CREATE DATABASE kartikidb;

# Create the Table
Run the following SQL commands to create the feedback table:

DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    department VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    feedback TEXT NOT NULL,
    attachment VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## Python Dependencies
List all dependencies in requirements.txt:
flask
psycopg2-binary

## Docker Setup

1️⃣ Build the Flask App Image
docker build -t python-app .

2️⃣ Run PostgreSQL Container
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=kartikidb \
  -e POSTGRES_USER=kartiki \
  -e POSTGRES_PASSWORD=kartiki \
  postgres:13

3️⃣ Create Feedback Table in PostgreSQL
docker exec -it postgres-db psql -U kartiki -d kartikidb

table is as follows:
DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    department VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    feedback TEXT NOT NULL,
    attachment VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Now, enter command     \dt
It shows a list of all tables in the current database and schema.
you might see something like:
             List of relations
 Schema |   Name    | Type  |  Owner
--------+------------+-------+---------
 public | feedback   | table | kartiki
(1 row)

4️⃣ Run Flask Container
docker container run \
  --name python-app \
  -p 5000:5000 \
  --link postgres-db:db \
  -e POSTGRES_HOST=db \
  -e POSTGRES_DB=kartikidb \
  -e POSTGRES_USER=kartiki \
  -e POSTGRES_PASSWORD=kartiki \
  python-app

## Docker Container Management Commands

🛑 Stop All Running Containers
docker stop $(docker ps -a -q)

🗑️ Remove All Stopped Containers
docker rm $(docker ps -a -q)

🧱 Stop a Specific Container
docker stop python-app

❌ Remove a Specific Container
docker rm python-app

🌐 Access the Application
Once both containers are running, open:
http://18.16.121.223:5000

You’ll see the Employee Feedback Portal where you can:
Submit feedback
View all employee responses

👩‍💻 Author
Kartiki Chandrashekhar Gaikwad
Technical Associate @ GSK GCC


