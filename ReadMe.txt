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

