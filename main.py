from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import json 
from pathlib import Path 

DATA_FILE = Path(__file__).parent / "heroes.json"

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


def load_heroes() -> list[Hero]:
    if not DATA_FILE.exists():
        return []
    
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return [Hero(**item) for item in raw]
    except json.JSONDecodeError:
        return []
    
def save_heroes(items: list[Hero]) -> None:
    payload = [h.model_dump() for h in items]
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)



""" heroes: List[Hero] = [
    Hero(
        id=str(uuid.uuid4()),
        name="Spider-Man",
        alter_ego="Peter Parker",
        power="Spider-sense, more",
        team="Avengers",
    )
] """

heroes: List[Hero] = load_heroes()

@app.get("/heroes")
def get_heroes():
    return heroes


@app.post("/heroes", status_code=201)
def create_hero(payload: HeroIn):
    hero = Hero(id=str(uuid.uuid4()), **payload.model_dump())
    heroes.append(hero)
    save_heroes(heroes)
    return hero

@app.put("/heroes/{hero_id}")
def update_hero(hero_id: str, payload: HeroIn):
    for i, hero in enumerate(heroes):
        if hero.id == hero_id:
            updated = Hero(id=hero_id, **payload.model_dump())
            heroes[i] = updated
            save_heroes(heroes)
            return updated
    raise HTTPException(status_code=404, details="hero not found")


@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: str):
    global heroes
    before = len(heroes)
    heroes = [h for h in heroes if h.id != hero_id]

    if len(heroes) == before:
        raise HTTPException(status_code=404, detail="Hero not found")
    save_heroes(heroes)
    return
