import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__ , url_prefix='/auth')


'''
    This creates a Blueprint named 'auth'. Like the application obj, the
    blueprint needs to know where it is defined, so __name__ is passed as
    the second argument. the url_prefix will be prepended to all the URLs
    associated with the blueprint.

    The auth bp will have views to register new users and to log in and out.
'''