import pytest
from flask import g, sesion
from flaskr.db import get_db 

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username':'a', password:'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

    
    @pytest.mark.parametrize(('username', 'password', 'message'),
                              ( ('', '', b'Username is required.'),
                                ('a', '', b'Password is required.'),
                                ('test', 'test', b'already registered'),
                              ))
    def test_register_validate_input(client, username, password, message):
        response = client.post(
            '/auth/register',
            data={'username': username, 'password': password}
        )
        assert message in response.data

    '''
      client.get() makes a GET request and returns the Response object returned
      by Flask. Similarly, client.post() makes a POST request, converting the data
      dict into form data.

      To test that the page renders successfully, a simple request is made and checked for
      a 200 OK status_code. If rendering failed, Flask would return a 500 Internal Server
      Error code.

      headers will have a Location header with the login URL, when the register view redirects
      to the login view.

      data contains the body of the response as bytes. If you expect a certain value to render the page
      check that it is in data. Bytes must be compared to bytes. If you want to compare
      text, use get_data(as_text=True) instead.

      pytest.mark.parametrize tells Pytest to run the same test function with different arugments.
      You use it here to test different invalid input and error messages without writing the same
      code three times.
    '''