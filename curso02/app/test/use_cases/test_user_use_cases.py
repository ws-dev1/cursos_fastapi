import pytest
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.schemas.user import User
from jose import jwt, JWTError
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases
from fastapi.exceptions import HTTPException
from app.db.models import User as UserModel
from decouple import config

SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')


crypt_context = CryptContext(schemes=['sha256_crypt'])

def test_register_user(db_session):
    
    user = User(
        username='Wesley',
        password='teste'
    )

    uc = UserUseCases(db_session)
    uc.register_user(user)


    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()

def test_register_user_existing_username(db_session):
    user_on_bd = UserModel(
        username='Wesley',
        password=crypt_context.hash('teste')
    )

    db_session.add(user_on_bd)
    db_session.commit()

    uc = UserUseCases(db_session)

    user = User(
        username='Wesley',
        password='teste'
    )
    with pytest.raises(HTTPException):
        uc.register_user(user=user)

    db_session.delete(user_on_bd)
    db_session.commit()


def test_user_login(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)
    user = User(username=user_on_db.username, password='teste')

    token_data = uc.user_login(user=user, expires_in=30)

    assert token_data.expires_at < datetime.utcnow() + timedelta(31)

def test_user_login_invalid_username(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)
    user = User(username='invalid', password='teste')

    with pytest.raises(HTTPException):
        uc.user_login(user=user, expires_in=30)

def test_user_login_invalid_password(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)
    user = User(username=user_on_db.username, password='invalid')

    with pytest.raises(HTTPException):
        uc.user_login(user=user, expires_in=30)


def test_verify_token(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    uc.verify_token(token=access_token)

def test_verify_token_expired(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.utcnow() - timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException):
        uc.verify_token(token=access_token)