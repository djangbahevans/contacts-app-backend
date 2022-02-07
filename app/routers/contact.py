import csv
from io import StringIO
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_

from .. import database, models, oauth2, schemas

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    new_contact = models.Contact(**contact.dict(), user_id=curr_user.id)

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


@router.post("/from-file")
def create_from_file(bt: BackgroundTasks, file: bytes = File(...), db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    def add_data_to_server():
        csv_string = file.decode('utf-8')
        buffer = StringIO(csv_string)
        csv_reader = csv.DictReader(buffer)

        pydantic_models: List[schemas.ContactCreate] = []
        for row in csv_reader:
            pydantic_models.append(schemas.ContactCreate(**row))

        sql_models: List[models.Contact] = []
        for model in pydantic_models:
            sql_models.append(models.Contact(**model.dict(), user_id=curr_user.id))

        db.add_all(sql_models)
        db.commit()
        
    bt.add_task(add_data_to_server)

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get('/', response_model=List[schemas.ContactResponse])
def get_contacts(response: Response, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user), per_page: int = 10, page: int = 0, search: str = ""):
    contacts = db.query(models.Contact).filter(
        and_(
            or_(
                models.Contact.given_name.contains(search),
                models.Contact.additional_name.contains(search),
                models.Contact.family_name.contains(search),
                models.Contact.name_prefix.contains(search),
                models.Contact.name_suffix.contains(search),
                models.Contact.location.contains(search),
                models.Contact.occupation.contains(search),
                models.Contact.notes.contains(search),
                models.Contact.email.contains(search),
                models.Contact.phone1.contains(search),
                models.Contact.phone2.contains(search),
                models.Contact.organization.contains(search),
                models.Contact.website.contains(search)
            ),
            models.Contact.user_id == curr_user.id
        )
    ).limit(per_page).offset(per_page*page).all()

    count = db.query(models.Contact).count()
    response.headers["x-total-count"] = f"{count}"

    return contacts


@router.get("/{id}", response_model=schemas.ContactResponse)
def get_contact(id: int, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    contact = db.query(models.Contact).filter(
        and_(models.Contact.id == id, models.Contact.user_id == curr_user.id)).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with ID: {id} was not found")

    return contact


@router.put("/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, updated_contact: schemas.ContactCreate, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    contact_query = db.query(models.Contact).filter(models.Contact.id == id)

    contact = contact_query.first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with ID: {id} was not found")

    if contact.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    contact_query.update(updated_contact.dict(), synchronize_session=False)
    db.commit()

    return contact_query.first()


@router.delete("/{id}")
def delete_contact(id: int, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    contact_query = db.query(models.Contact).filter(models.Contact.id == id)

    contact = contact_query.first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with ID: {id} was not found")

    if contact.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    contact_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
