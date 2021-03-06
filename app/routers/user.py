from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from redis import Redis
from sqlalchemy.orm.session import Session

from app.constants import FORGOT_PASSWORD_PREFIX, USER_PREFIX

from .. import database, models, oauth2, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with the same email already exists")

    hashed_password = utils.hash(user.password.get_secret_value())
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=schemas.UserResponse)
def get_current_user(db: Session = Depends(database.get_db), curr_user: models.User = Depends(oauth2.get_current_user)):
    return curr_user


@router.put("/{id}/reset-password")
def update_user_password(id: int, body: schemas.PasswordUpdate, db: Session = Depends(database.get_db), redis: Redis = Depends(database.get_cache)):
    token = body.token
    password = body.password

    hash = redis.get(f"{USER_PREFIX}:{FORGOT_PASSWORD_PREFIX}:{id}")
    if not hash:  # Token doesn't exist
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not utils.verify(token, hash):  # Token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Token exists for the selected user that means we can update password
    hashed_password = utils.hash(password.get_secret_value())

    db.query(models.User).filter(models.User.id == id).update(
        {"password": hashed_password}, synchronize_session=False)

    # delete token
    redis.delete(f"{USER_PREFIX}:{FORGOT_PASSWORD_PREFIX}:{id}")
    db.commit()

    return {"data": "Password updated successfully"}
