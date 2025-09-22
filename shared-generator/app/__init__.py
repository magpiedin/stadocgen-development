from flask import Flask

def create_app(config):
    """
    Application factory for the site generator.

    Takes a loaded YAML config and creates a Flask app instance.
    """
    # The template folder is relative to the app's root path.
    app = Flask(__name__, template_folder='templates')

    # Store the config in the Flask app object for easy access in views
    app.config['GENERATOR_CONFIG'] = config

    # Import and register the routes
    from . import routes
    routes.register_routes(app)

    return app
