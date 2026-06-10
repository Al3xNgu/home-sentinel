from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonResponse, PersonUpdate

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

@router.get("/people", response_model=list[PersonResponse])
def get_people(db: Session = Depends(get_db)):
    people = db.query(Person).order_by(Person.id).all()
    return people

@router.get("/people/{person_id}", response_model=PersonResponse)
def get_person(
    person_id: int,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )
    
    return person

@router.delete("/people/{person_id}", response_model=PersonResponse)
def delete_person(
    person_id: int,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    db.delete(person)
    db.commit()
    return person

@router.put("/people/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: int,
    person_data: PersonUpdate,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )
    
    person.name = person_data.name
    db.commit()
    db.refresh(person)
    return person


