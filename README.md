# Student Management System

## About the Project
This project is a simple web-based Student Management System built using Flask and SQLite. The goal was to create a basic system where student records can be added, viewed, updated, and deleted through a user-friendly interface.
While building this, I focused on understanding how backend logic connects with a database and how data can be displayed dynamically on a web page.

---

## Features
* Login system for basic authentication
* Add new student records
* View all students in a structured table
* Edit student details
* Delete records when needed
* Automatic grade calculation based on marks
* Status indicator based on performance and attendance
* Input validation to avoid incorrect data
* Graph visualization of student marks.

---

## Technologies Used
* **Python (Flask)** – backend logic
* **SQLite** – database
* **HTML & CSS** – frontend design
* **Chart.js** – for graph visualization

---

## Project Structure

```text
student_management_system/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── add.html
│   ├── edit.html
│   ├── view.html
│   └── graph.html
│
├── main.py
├── students.db
└── README.md
```
---
## What I Learned
While working on this project, I learned:
* How to build a basic CRUD application using Flask
* Connecting Python with a database (SQLite)
* Handling form data and validations
* Managing sessions for login functionality
* Rendering dynamic data in HTML using templates
* Displaying data visually using charts
---

## Challenges Faced
Some issues I faced during development:
* Handling form validation properly
* Passing data from Flask to JavaScript for graphs
* Fixing template rendering errors
* Debugging JavaScript chart issues

Working through these helped me understand how frontend and backend interact.
---

## Conclusion
This project helped me strengthen my understanding of full-stack basics and gave me hands-on experience in building a functional web application from scratch.

