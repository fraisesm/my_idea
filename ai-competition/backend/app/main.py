from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os
from pathlib import Path
from .database import engine, SessionLocal
from .models import Base, Team, Task, Solution
from .schemas import TeamCreate, SolutionCreate, SolutionStatus
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# WebSocket connections
active_connections = {}

# Load tasks
TASKS_DIR = Path(__file__).parent / "data" / "tasks"
tasks = []

def load_tasks():
    global tasks
    tasks = []
    for i, task_file in enumerate(sorted(TASKS_DIR.glob("*.json"))):
        with open(task_file) as f:
            task_data = json.load(f)
            tasks.append({
                "id": str(i + 1),
                "data": task_data
            })

@app.on_event("startup")
async def startup_event():
    load_tasks()
    asyncio.create_task(task_distributor())

async def task_distributor():
    while True:
        await asyncio.sleep(30)
        for task in tasks:
            for connection in active_connections.values():
                await connection.send_json({
                    "type": "task",
                    "task_id": task["id"],
                    "data": task["data"]
                })

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=TeamCreate)
async def register_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == team.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already registered")
    
    team_id = str(uuid.uuid4())
    db_team = Team(
        id=team_id,
        name=team.name,
        password_hash=team.password + "_hash",  # In production, use proper hashing
        email=team.email
    )
    db.add(db_team)
    db.commit()
    return {"id": team_id, **team.dict()}

@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: str):
    await websocket.accept()
    active_connections[team_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "solution":
                db = SessionLocal()
                try:
                    db_solution = Solution(
                        id=str(uuid.uuid4()),
                        team_id=team_id,
                        task_id=data["task_id"],
                        answer=json.dumps(data["solution"]),
                        status=SolutionStatus.SUBMITTED,
                        timestamp=datetime.now()
                    )
                    db.add(db_solution)
                    db.commit()
                finally:
                    db.close()
    except WebSocketDisconnect:
        active_connections.pop(team_id, None)

@app.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    solutions = db.query(Solution).all()
    
    return {
        "teams": [{"id": t.id, "name": t.name} for t in teams],
        "solutions": [
            {
                "team_id": s.team_id,
                "task_id": s.task_id,
                "status": s.status,
                "timestamp": s.timestamp.isoformat()
            } for s in solutions
        ]
    }