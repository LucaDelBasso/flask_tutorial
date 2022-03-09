import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


'''
   g is a special object that is unique for each request.
   It is used to store data that might be accessed by multiple
   functions during the request.

   The connection is stored and reused instead of creating
   a new connection if get_db is called a second time
   in the same request.

   current_app is another special object that points to the Flask
   application handling the request. Since using an application
   factory, there is no application object when writing the
   rest of the code. get_db will be called when the application
   has been created and is handling a request, so current_app 
   can be used.
'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_ap.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        #this tells the connection to return rows that behave
        #like dicts. Allows for accessing the columns by name
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    '''
      checks if a connection was created by checking if g.db
      was set. If the connection exists, it is closed. Further
      along, application gets told about close_db in the app factory
      so that it is called after each request.
    '''
    
    db = g.pop('db', None)

    if db is not None:
        db.close()
