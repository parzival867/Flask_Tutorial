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

Register the init_db_command and close_db functions
    ->  app.teardown_appcontext() tells flask to call the function when
        cleaning up after returning the response
    ->  app.cli.add_command() adds a new command that can be called with the
        flask command
-----------------------------------------------------------------------------------------

Blueprints and Views

Blueprint:
    ->  organize a group of related views and other code.
    ->  views and code registered with a blueprint.
    ->  then the bluepring is registered with the application when available in
        factory function

Views:
    ->  the code to respond to requests
    ->  returns data that the flask turns into an outgoing respone

Flaskr has two blueprints (each in separate module):
    1.  for the authentication functions
        
        view 1: Register
                
                *   @bp.route associates the URL /register with the view
                *   function
                *   ->  when flask receives a request to /auth/register, it
                *       will call the register view
                *   If the form was submitted , the request would be POST
                *   
                *   request.form is a special type of dict mapping submitted
                *   form keys and values.
                *
                *   Validate that username and password are not empty
                *
                *   Validate that username is not taken by querying the
                *   database with db.execute
                *   fetchone() returns one row from the query. if there are no
                *   results, it returns None.
                *   fetchall() used later and returns a list of all results
                *   
                *   If validation succeeds, insert the new user data into the
                *   database.
                *   never store passwords directly, use generate_hash
                *   db.commit() needs to be called to save changes
                *
                *   After storing the user, redirected to the login page.
                *   url_for() generates the URL for the login view.
                *   
                *   If validation fails, the error is shown to the user.
                *   flash() stores messages that can be retrieved when
                *   rendering the template
                *
                *   initial navigation to auth/register  or if there was
                *   validation error, then render_template shows HTML page with
                *   the registration form

        view 2: Login
            
            *   user is queried firs and stored in a variable for later use
            *   
            *   check_password_hash() hashes submitted password in the same way
            *   as the stored  hash and securely compare them
            *
            *   session is a dict that stores data across requests, if
            *   validation succeeds the user's id is stored in a new session.
            *   The data is storen in  a cookie sent to the browser.
        
        view 3: before app request
            
            *   bp.before_app_request register a function that runs before the
            *   view function.
            *   load_logged_in_user checks if there is a user id stored in the
            *   session and gets the user's data form the database and store it
            *   in g.user
            *   g.user lasts for the length of the request
