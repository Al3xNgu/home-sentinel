from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import shutil
from uuid import uuid4
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonResponse, PersonUpdate
from app.models.person_photo import PersonPhoto
from app.schemas.person_photo import PersonPhotoResponse
from app.services.face_service import validate_single_face

router = APIRouter()

# people CRUD routes
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

# photo routes
@router.post("/people/{person_id}/photos", response_model=PersonPhotoResponse)
def upload_person_photo(
    person_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )
    
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed"
        )

    upload_dir = Path("uploads") / "people" / str(person_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    is_valid, error_message = validate_single_face(str(file_path))

    if not is_valid:
        file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=error_message
        )

    photo = PersonPhoto(
        person_id=person_id,
        image_path=str(file_path)
    )

    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo

@router.get("/people/{person_id}/photos", response_model=list[PersonPhotoResponse])
def get_person_photos(
    person_id: int,
    db: Session = Depends(get_db)    
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return person.photos

@router.delete("/people/{person_id}/photos/{photo_id}", response_model=PersonPhotoResponse)
def delete_person_photo(
    person_id: int,
    photo_id: int,
    db: Session = Depends(get_db)
):
    photo = db.query(PersonPhoto).filter(
        PersonPhoto.id == photo_id, 
        PersonPhoto.person_id == person_id
    ).first()

    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )
    
    file_path = Path(photo.image_path)

    if file_path.exists():
        file_path.unlink()
    
    db.delete(photo)
    db.commit()

    return photo