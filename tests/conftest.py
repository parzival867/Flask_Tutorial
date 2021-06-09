import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

""" For most views, the user needs to be logged in.
    To do this in tests, make a POST request to the login 
    write a class with methods to that and a fixture to pass it the client for
    each test
    """

class AuthActions(object):
    def __init__(self, client):
        self.__client = client

    def login(self, username='test', password='test'):
        return self._client.post(
                '/auth/login',
                data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

""" with the auth fixture, can call auth.login() in a test to log in as the
test user.
The register view should render successfully on GET. 
On POST with valid form data, it should redirect to the login URL and the
user's data should be in the database. Invalid data should display error
messages """



