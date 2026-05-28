from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select
from typing_extensions import TypedDict

from connection import get_session, init_db
from models import (
    Profession,
    ProfessionCreate,
    Skill,
    SkillCreate,
    SkillWarriorLink,
    SkillWarriorLinkCreate,
    Warrior,
    WarriorDefault,
    WarriorWithRelations,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=WarriorWithRelations)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@app.post("/warrior")
def warriors_create(
    warrior: WarriorDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Warrior}):
    db_warrior = Warrior.model_validate(warrior)
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return {"status": 200, "data": db_warrior}


@app.patch("/warrior/{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> Warrior:
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    warrior_data = warrior.model_dump(exclude_unset=True)
    for key, value in warrior_data.items():
        setattr(db_warrior, key, value)

    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior


@app.delete("/warrior/delete/{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    profession = session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession


@app.post("/profession")
def profession_create(
    prof: ProfessionCreate, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Profession}):
    db_prof = Profession.model_validate(prof)
    session.add(db_prof)
    session.commit()
    session.refresh(db_prof)
    return {"status": 200, "data": db_prof}


@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@app.post("/skill")
def skill_create(
    skill: SkillCreate, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Skill}):
    db_skill = Skill.model_validate(skill)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return {"status": 200, "data": db_skill}


@app.post("/warrior-skill-link")
def create_warrior_skill_link(link: SkillWarriorLinkCreate, session=Depends(get_session)):
    warrior = session.get(Warrior, link.warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    skill = session.get(Skill, link.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    exists = session.get(SkillWarriorLink, (link.skill_id, link.warrior_id))
    if exists:
        return {"ok": True, "message": "Link already exists"}

    db_link = SkillWarriorLink(skill_id=link.skill_id, warrior_id=link.warrior_id)
    session.add(db_link)
    session.commit()
    return {"ok": True}


@app.delete("/warrior-skill-link")
def delete_warrior_skill_link(warrior_id: int, skill_id: int, session=Depends(get_session)):
    link = session.get(SkillWarriorLink, (skill_id, warrior_id))
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    session.delete(link)
    session.commit()
    return {"ok": True}