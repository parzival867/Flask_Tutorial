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

        view 4: Logout

            *   remove the user from session


        Require Authentication on other viwew
            
            *   use decorator
            *   returns a new funtion that wraps funtion that 



        Enpoints and URLS
            
            The url_for() function generates the URL to a view based on a name
            and arguments. The name associated with a view is also called the
            endpoint, and by default is the same as the name of the view
            functon.

            hello() view added to app factory has the name 'hello' and can be
            linked to with url_for('hello')
            if it took an argurment, url_for('hello', who='World')

            when using blueprint, the name of the blueprint is added to the
            front of the name of the function
            endpoint for the login function: auth.login
    2.  For the blog:

        in __init__.py:
            blog does not have a url_prefix, so the index view will be at /
            and create view will be ant /create

            the endpoint forthe index view will be blog.index
            app.add_url_rule() associates the enpoint name'index' with the /
            url so url_for('index') and url_for('blog.index') will both
            generate / URL

            *** in another app, may give the blog bluepring a url_prefix and
            define a separate index view in the application factory, similar to
            the hello view.

        View 1: Index

            *   The index shows all the posts
            *
            *   JOIN  is used so that the author information from the user
            *   table is available

        View 2: Update

            *   update function takes an argument, id
            *   url will look like /1/update

---------------------------------------------------------------------------------------------

Templates:

*   base.html

        g is automatically available in templates.

        If g.user is set (from load_logged_in_user) different links are
        displayed in header

        url_for() is also automatically available, and is  used to generate
        URLs to the views.

        flash() was used in views to show error messages so looping over the
        messages returned by get_flashed_messages() will display them

*   register.html
        
        {% extends 'base.html' %} tells Jinja to replace the blocks from the
        base template.

        placing {% block title %} inside {% block header %} sets the title
        block and then outputs the value into the header block, so that the
        window and the page share the same title without writing it twice

        even though the required attribute ensures fields are filled in, still
        need to validate data on server, because some browsers may not support
        attribute etc.

*   login.html

        identical basically to register.html

--------------------------------------------------------------------------------

Making project installable:

setup.py    

    *   packages tells Python what package directories to include
        find_packages() finds them automatically 

MANIFEST.in
    
    *   tells python to copy everythin in the static and template directories
        and the schema.sql file

------------------------------------------------------------------------

Testing

    *   tempfile.mkstemp() creates and opens a temporar file,returning the file
    *   descriptor.

    *   the DATABASE path is overridded so it points to this temporary path
    *   instead of the instance folder. After setting the pat, the database
    *   tables are created and the test data is inserted. The temporary file is
    *   closed and removed when the test is over.

    *   TESTING tells flask that the app is in test mode.

    *   the client fixture calls app.test_client() with the application object
    *   created by the app fixture. Tests will use the client to make requests
    *   to the application without running the server

    *   the runner fixture is similar to client.
    *   app.test_cli_runner() creates a runner that can cll the Click commands
    *   registered with the application

    *   Pytest uses fixtures by matching their function names with the names of
    *   arguments in the test functions.


-------------------------------------------------------------

Deploying

*   To deploy application elsewhere, build a distribution file. 
    use wheel format -> .whl

    install wheel library first:
    pip install wheel

    build wheel distribution file using setup.py
    'python setup.py bdist_wheel'

    the file is in:
    dist/flaskr-1.0.0-py3-none-any.whl
    {project name}-{version}-{python tag}-{abi tag}-{platform tag}

    Copy to another machine set up new virtualenv
    and install with pip
    'pip install flaskr-1.0.0-py3-none-any.whl'

    run 
    '$env: FLASK_APP = 'flaskr' '
    'flask init-db'

    instances will be in a different directory
    'venv/var/flaskr-instance'


    Change secret key

    flaskr-instance/config.py
        SECRET_KEY = b';lpioboj;n'


Don't use 'flask run' (built in development server)
instead use production WSGI server eg: Waitress
    ->  pip install waitress

    tell server to import and call the application factory 
    to get an application object

    eg. waitress-serve --call 'flaskr:create_app'
