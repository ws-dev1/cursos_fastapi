import pytest
from datetime import datetime
from app.schemas.user import User, TokenData


def test_user_schemas():
    user = User(username='Wesley', password='teste')

    assert user.dict() == {
        'username': 'Wesley',
        'password': 'teste'
    }


def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(username='João#', password='teste')

def test_token_data():
    expires_at= datetime.now()
    token_data = TokenData(
        access_token='token',
        expires_at= expires_at
    )

    assert token_data.dict() =={
        'access_token': 'token',
        'expires_at':expires_at
    }
