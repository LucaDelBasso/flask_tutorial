import os

from flask import Flask

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    ''' 
        __name__ is the name of the current python module.
        The app needs to know where it is located to set up
        some paths, and __name__ is a convinent way to tell it that.

        instance_relative_config=True tells the app that configuration
        files are relative to the instance folder. The instance folder
        is located outside the flaskr package and can hold local data that
        shouldn't be committed to version control, such as config secrets 
        and the database file.
    
    '''
    print("NAME!:" , __name__)

    app.config.from_mapping(
        SECRET_KEY='DEV',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    '''
        SECRET_KEY is used by Flask and extensions to keep data safe.
        It's set to 'dev' to provide a convenient value during development,
        but it should be overriden with a random value when deploying.

        DATABASE is the path where the SQLite db file will be saved.
        it's under app.instance_path, which is the path that Flask has
        chosen for the instance folder. 
    '''



    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        '''
            app.config.from_pyfile overrides the default config with values
            taken from the config.py file in the instance folder if it exists.
            Can set a secret key here and because instance folder goes in
            .gitignore people won't be able to see it.

                test config can also be passed to the factory, and will be 
                used instead of the instance config. This is so the tests 
                written later can be configured independently of any dev values
                that are configured
        '''
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #esnure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        '''
            this ensures that app.instance_path exists. Flask doesn't create
            the instance folder automatically, but it needs to be created because
            the project will create the SQLite db file there
        '''
    except OSError:
        pass

    #a simple page that says hello
    '''
        @app.route() creates a simple route so you can see the app
        working before developing any further. It creates a connection
        between the URL /hello and a function that returns a response
    '''
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #register the db with the application
    from . import db 
    db.init_app(app)

    #register the auth blueprint with the application
    from .import auth
    app.register_blueprint(auth.bp)

    return app