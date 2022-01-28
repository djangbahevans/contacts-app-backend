import secrets
from typing import Optional

from app.config import settings
from fastapi import APIRouter, BackgroundTasks, Header, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
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


@router.post("/password-reset")
def reset_password(email: schemas.Email, bt: BackgroundTasks, db: Session = Depends(database.get_db), user_agent: Optional[str] = Header(None)):
    # Check if email exists
    user = db.query(models.User).filter(
        models.User.email == email.email).first()
    print("USER_AGENT", user_agent)
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
        
        bt.add_task(utils.send_email, recipient=email.email,
                    subject="Reset your Contacts App password", template='password_reset_help.html', payload=payload)
        return {"data": "A password reset link has been sent to your email"}

    # check if user has token and delete it if user has
    db.query(models.Token).filter(models.Token.user_id ==
                                  user.id).delete(synchronize_session=False)

    # Create new token
    reset_token = secrets.token_hex(32)
    hash = utils.hash(reset_token)

    token = models.Token(token=hash, user_id=user.id)
    db.add(token)
    db.commit()
    db.refresh(token)

    payload = {
        "name": user.email,
        "product_name": "Contacts App",
        "operating_system": ua.get_os(),
        "browser_name": ua.get_browser(),
        "email_address": email.email,
        "action_url": f"{settings.frontend_domain}/reset-password?token={reset_token}",
        "support_url": "tel:+233501360696",
        "company_name": "Evans and Sons",
    }
    bt.add_task(utils.send_email, recipient=email.email,
                subject="Reset your Contacts App password", template='password_reset.html', payload=payload)

    return {"data": "A password reset link has been sent to your email"}
