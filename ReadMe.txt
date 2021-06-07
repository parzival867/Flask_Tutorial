----------------------------------------------------
__init__.py

create_app is the application factory function.

app = Flask(__name__, instance_relative_config=True)
    -> creates the Flask instance

    __name__ 
        ->  name of the current Python module

    instance_relative_config=True
        ->  tells app that configuration files are stored
            in the instance folder

app.config.from_mapping()
    ->  sets some default configuration:

    SECRET_KEY
        ->  used to keep data safe, 
        ->  set to dev for development

    DATABASE
        ->  path where SQLite db file will be saved
        ->  under app.instance_path

app.config.from_pyfile()
    ->  overides default config with values 
    ->  taken from config.py, can be used to set a real secret key

    test_config
        ->  used so tests can be configured independently of develpment values

os.makedirs()
    ->  dnsures that app.instance_path exists

------------------------------------------------------------------------------------------------
db.py

The first thing to do when working with SQLite db is to create a connection to
it
the connection is tied to the request.
    ->  created at some point when handling the request
    ->  closed before the request is sent


g is a special object that is unique for each request.
Stores data that might be accessed by multiple functions during the request
    ->  connection is stored and reused if get_db is called a second time in
        request

current_app is another special object that points to the Flask application
handling the request.
    ->  no application object when writing rest of code because of app factory
    ->  get_db will be called when the applicaton has been created and 
        is handling a request, so current_app can be used

sqlite3.connect() 
    ->  establishes a connection to the file pointed at by the DATABASE config
        key

sqlite3.Row 
    ->  tells the connection to return rows that behave like dicts.
    ->  so can access columns by name

close_db checks if g.db was set

open_resource()
    ->  opens file relative to flaskr
    ->  get_db return a database connection, used to execute commands 

click.command()
    ->  defies a command line command called init-db that calls init_db
    ->  and shows success message
-----------------------------------------------------------------------------------------
