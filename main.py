import os
from fastapi import FastAPI,Depends
from database import engine, Base,SessionLocal
from sqlalchemy.orm import Session
import models, schemas
from utils import hash_password
from utils import verify_password
from auth import create_access_token
from fastapi import Header, HTTPException
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from fastapi import File, UploadFile, Depends
import shutil
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Header(...)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/profile")
def profile(user: str = Depends(get_current_user)):
    return {"message": f"Welcome {user}"}



@app.get("/")
def home():
    return {"message": "Video Streaming Backend API Running"}

@app.get("/videos")
def get_videos():
    return {"videos": []}

@app.get("/tasks")
def get_tasks():
    return {"tasks": []}


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        return {"error": "Email already registered"}

    hashed_password = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/upload-video")
def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    # get logged-in user
    user = db.query(models.User).filter(models.User.email == user_email).first()

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_video = models.Video(
        title=file.filename,
        description="Uploaded video",
        file_path=file_location,
        uploaded_by=user.id
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return {"message": "Video uploaded successfully"}

@app.get("/my-videos")
def get_my_videos(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    # get logged-in user
    user = db.query(models.User).filter(models.User.email == user_email).first()

    # get videos of that user
    videos = db.query(models.Video).filter(models.Video.uploaded_by == user.id).all()

    return videos

@app.post("/tasks")
def create_task(
    title: str,
    description: str,
    status: str,
    video_id: int,
    db: Session = Depends(get_db)
):
    new_task = models.Task(
        title=title,
        description=description,
        status=status,
        video_id=video_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    return task
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.status = status
    db.commit()

    return {"message": "Task updated"}
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}