from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Сущест=вующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get('/api/v1/user', params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    response = client.get('/api/v1/user', params={'email': 'ghost@example.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
    pass


def test_create_user_with_valid_email():
    payload = {'name': 'Test User', 'email': 'test@example.com'}
    response = client.post('/api/v1/user', json=payload)
    assert response.status_code == 201
    assert isinstance(response.json(), int)
    pass


def test_create_user_with_invalid_email():
    payload = {'name': 'Duplicate User', 'email': users[0]['email']}
    response = client.post('/api/v1/user', json=payload)
    assert response.status_code == 409
    pass


def test_delete_user():
    payload = {'name': 'Delete User', 'email': 'delete@example.com'}
    client.post('/api/v1/user', json=payload)
    response = client.delete('/api/v1/user', params={'email': payload['email']})
    assert response.status_code == 204
    pass
