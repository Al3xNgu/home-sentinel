from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonResponse

router = APIRouter()

@router.post("/people", response_model=PersonResponse)
def create_person(
    person_data: PersonCreate,
    db: Session = Depends(get_db)
):
    person = Person(name=person_data.name)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person