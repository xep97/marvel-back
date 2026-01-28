from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Depends
from pydantic import BaseModel
from pathlib import Path 
from typing import List
from sqlalchemy.orm import Session
from models import HeroDB
from db import SessionLocal
import uuid
import json 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DATA_FILE = Path(__file__).parent / "heroes.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

class HeroIn(BaseModel):
    name: str
    alter_ego: str
    power: str
    team: str

class Hero(HeroIn):
    id: str



# heroes: List[Hero] = load_heroes()

@app.get("/heroes")
def get_heroes(db: Session = Depends(get_db)):
    rows = db.query(HeroDB).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "alter_ego": r.alter_ego,
            "power": r.power,
            "team": r.team,
        }
        for r in rows
    ]


@app.post("/heroes", status_code=201)
def create_hero(payload: HeroIn, db: Session = Depends(get_db)):
    row = HeroDB(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(row)
    db.commit()
    return [
        {
            "id": row.id,
            "name": row.name,
            "alter_ego": row.alter_ego,
            "power": row.power,
            "team": row.team,
        }
    ]

@app.put("/heroes/{hero_id}")
def update_hero(hero_id: str, payload: HeroIn):
    for i, hero in enumerate(heroes):
        if hero.id == hero_id:
            updated = Hero(id=hero_id, **payload.model_dump())
            heroes[i] = updated
            # save_heroes(heroes)
            return updated
    raise HTTPException(status_code=404, details="hero not found")


@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: str):
    global heroes
    before = len(heroes)
    heroes = [h for h in heroes if h.id != hero_id]

    if len(heroes) == before:
        raise HTTPException(status_code=404, detail="Hero not found")
    # save_heroes(heroes)
    return
