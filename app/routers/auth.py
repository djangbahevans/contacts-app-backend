import secrets
from typing import Optional

from app.config import settings
from app.constants import FORGOT_PASSWORD_PREFIX, USER_PREFIX
from fastapi import APIRouter, BackgroundTasks, Header, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from redis import Redis
from sqlalchemy.orm.session import Session
from user_agents import parse

from .. import database, models, oauth2, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def reset_password(email: schemas.Email, bt: BackgroundTasks, db: Session = Depends(database.get_db), user_agent: Optional[str] = Header(None), redis: Redis=Depends(database.get_cache)):
    msg = "A password reset message was sent to your email address. Please click the link in that message to reset your password."
    # Check if email exists
    user = db.query(models.User).filter(
        models.User.email == email.email).first()

    ua = parse(user_agent_string=user_agent)

    if not user:
        # Send email to the current email and return
        payload = {
            "product_name": "Contacts App",
            "operating_system": ua.get_os(),
            "browser_name": ua.get_browser(),
            "email_address": email.email,
            "action_url": f"{settings.frontend_domain}",
            "support_url": "tel:+233501360696",
            "company_name": "Evans and Sons",
        }

        bt.add_task(utils.send_email, recipients=[email.email],
                    subject="Reset your Contacts App password", template='password_reset_help.html', payload=payload)
        return {"data": msg}

    # Delete any existing token
    redis.delete(f"{USER_PREFIX}:{FORGOT_PASSWORD_PREFIX}:{user.id}")

    # Create new token
    reset_token = secrets.token_hex(32)
    hash = utils.hash(reset_token)
    
    redis.set(f"{USER_PREFIX}:{FORGOT_PASSWORD_PREFIX}:{user.id}", hash, ex=24*60*60)

    payload = {
        "name": user.email,
        "product_name": "Contacts App",
        "operating_system": ua.get_os(),
        "browser_name": ua.get_browser(),
        "email_address": email.email,
        "action_url": f"{settings.frontend_domain}/reset-password?token={reset_token}&user_id={user.id}",
        "support_url": "tel:+233501360696",
        "company_name": "Evans and Sons",
    }
    bt.add_task(utils.send_email, recipients=[email.email],
                subject="Reset your Contacts App password", template='password_reset.html', payload=payload)

    return {"data": msg}
