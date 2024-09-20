from fastapi import FastAPI , HTTPException,Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .models import User, Task
from datetime import date


app = FastAPI()

session = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Aquí pones el origen exacto de tu frontend
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

class Auth(BaseModel):
    email: str
    password: str



# @app.get("/auth/session")
# async def checkSession(user= Depends(getUser)):
#     return {"authenticated": True, "user": user.email}

@app.post("/auth/login")
async def login(auth: Auth): 
    user = User.objects(email=auth.email, password=auth.password).first()
    if user:
        session['user'] = user.email
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}

def getUser():
    if 'user' in session:
        user = User.objects(email=session['user']).first()
        return user
    return None

@app.get("/auth/session")
async def checkSession():
    user = getUser()
    if user:    
        return {"authenticated": True, "user": user.email}
    
    
@app.post("/auth/register")
async def signup(auth: Auth):  
    if User.objects(email=auth.email).first():
        return {"message": "User already exists"}
    else:
        user = User.createUser(email=auth.email, password= auth.password, username= auth.email)
        return {"message": auth.email}

class TaskBase(BaseModel):
    taskName: str
    category: str
    dueDate: date
    
@app.post("/tasks")
async def create_task(task: TaskBase):
    user = getUser()
    try:
        new_task = Task.create_task(task=task.taskName, category=task.category, dueDate=task.dueDate, user=user)
        return {"message": "Task created"}
    except Exception as e:
        return {"message": e.message}



@app.get("/task")
async def getTasks():
    user = getUser()  # Asumiendo que esta función obtiene el usuario actual
    tasks = Task.objects(user="66ecfa661f303c9e2b7c9556")
    print("Tasks fetched from DB:", tasks)

    # Convertimos los objetos en diccionarios JSON-serializables
    return [{"taskName": t.task, "category": t.category, "dueDate": t.dueDate.strftime("%Y-%m-%d")} for t in tasks]