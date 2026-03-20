# 🎥 Video Streaming Backend API

## 📌 Project Overview

This project is a **backend system for a video streaming platform** where users can register, log in, upload videos, stream them, and manage related tasks.

It is designed to simulate real-world applications like YouTube or Netflix by implementing authentication, file handling, and database operations.

---

## 🚀 Features

### 🔐 Authentication & User Management

* User Signup and Login
* Secure password hashing
* Token-based authentication using JWT

### 🎥 Video Management

* Upload videos to server
* Store video details in database
* Stream videos directly in browser

### 📋 Task Management (CRUD)

* Create tasks related to videos
* Read all tasks / specific task
* Update task status (pending, completed, etc.)
* Delete tasks

### 🔍 Filtering

* Filter tasks by status
* Get tasks based on video ID

---

## 🧱 Tech Stack

### Backend

* Python
* FastAPI

### Database

* MySQL

### ORM

* SQLAlchemy

### Authentication

* JWT (JSON Web Token)

### Security

* bcrypt (password hashing)

### File Handling

* Python (os, shutil)

---

## 🗂 Project Structure

```
video_stream/
 ├── main.py
 ├── models.py
 ├── schemas.py
 ├── database.py
 ├── utils.py
 ├── auth.py
 ├── uploads/          # stores uploaded videos
```

---

## ⚙️ How It Works

1. **User Registration**

   * User signs up with name, email, and password
   * Password is hashed before storing in database

2. **Login**

   * User logs in with credentials
   * Server verifies password and returns JWT token

3. **Authentication**

   * Token is used to access protected APIs
   * Ensures only authorized users can perform actions

4. **Video Upload**

   * User uploads video file
   * File is stored in `uploads/` folder
   * File path is saved in database

5. **Video Streaming**

   * API retrieves video file from server
   * Browser plays the video

6. **Task Management**

   * Tasks are created for videos
   * Supports full CRUD operations
   * Tasks can be filtered by status or video

---

## ▶️ API Endpoints

### Authentication

* `POST /signup`
* `POST /login`

### Videos

* `POST /upload-video`
* `GET /stream/{video_id}`
* `GET /my-videos`

### Tasks

* `POST /tasks`
* `GET /tasks`
* `GET /tasks/{task_id}`
* `PUT /tasks/{task_id}`
* `DELETE /tasks/{task_id}`
* `GET /tasks/filter?status=...`
* `GET /tasks/video/{video_id}`

---

## 🧪 Testing

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

---

## 💡 Key Learnings

* Building REST APIs using FastAPI
* Implementing authentication using JWT
* Securing passwords with hashing
* Handling file uploads and storage
* Designing relational databases
* Implementing CRUD operations
* Structuring real-world backend systems

---

## 🎯 Conclusion

This project demonstrates the development of a **complete backend system** including authentication, video handling, and task management. It reflects real-world backend architecture and is suitable for showcasing backend development skills.

---

## 📬 Future Improvements

* Add frontend (React)
* Deploy on cloud (AWS / Render)
* Add video compression & processing
* Use cloud storage (S3)

---
