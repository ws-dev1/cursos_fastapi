from decouple import config
from fastapi import Depends
from app.db.connection import Session
from sqlalchemy.orm import Session as SessionOrm
from fastapi.security import OAuth2PasswordBearer
from app.use_cases.user import UserUseCases

oauth_scheme= OAuth2PasswordBearer(tokenUrl='/user/login')

TEST_MODE =config('TEST_MODE')

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def auth(db_session: SessionOrm = Depends(get_db_session), token = Depends(oauth_scheme)):
    if TEST_MODE:
        return
    uc = UserUseCases(db_session=db_session)
    uc.verify_token(token=token)