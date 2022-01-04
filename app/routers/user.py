from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {id} does not exist")

    if user.id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="NotF authorized to perform requested action")

    return user
