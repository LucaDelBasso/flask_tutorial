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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    ''' 
        @bp.route associates the URL /register with the register view func.
        When Flask receives a request to /auth/register, it will call the register
        view and use the return value as the response.

        If the user submits the form, request.method will be 'POST'. In this case,
        start validating the input.

        request.form is a special type of dict mapping submitted form keys and values.
        The user inputs their username and password.

        redirect(url_for()) generates a redirect response to the generated url.
            url_for generates the URL for the login view based on its name.
                This is preferred to typing the URL directly as it allows for
                changes elsewhere without changing all code that links to it.
    
        When the user initially navigates to auth/register , or there is a validation
        error, a HTML page with the registration form should be shown (the return).
        if no validation error then retun the login page.
    '''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                # The query modifies data, db.commit() is called to save
                # the changes
                db.commit()
            except db.IntegrityError:
                error = f"Users {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        #flash stores messages that can be retrieved when rendering the template
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    ''' 
        The user is queried first and stored in a variable for later use.

        fetchone() returns one row from the query. None is returned if there
        are no results.

        check_password_hash() hashes the submitted password in the same way as 
        stored and compares them.

        session is a duct that stores data across reqeusts. When validation 
        succeeds, the user's id is stored in a new sesion. The data is stored 
        in a cookie that is sent to the browser, and the browser then sends it back
        with the subsequent request. Flask securly signs the data so it cant be
        tampered with.
    '''

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
    
        if error is None:
            session.clear()
            #store user_id in the sesson, it will now be available on
            #subsequent requests. 
            session['user_id'] = user['id']
            #if a user is logged in, their info should be loaded and made
            #available to other views.
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


'''
    bp.before_app_request() registers a function that runs before the view
    function, no matter what URL is requested.
'''
@bp.before_app_request
def load_logged_in_user():
    ''' 
        load_logged_in_user checks if a user id is stored in the session and 
        gets that user's data from the database, storing it on g.user, which
        lasts for the length of the request.
    '''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(index))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view