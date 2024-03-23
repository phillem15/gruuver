import os
import sys

from flask import Flask
from .cyanite import cyanite as cyanite_blueprint


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


def create_app(test_config=None):
    app = Flask(__name__)

    # Initialize our ngrok settings into Flask
    app.config.from_mapping(
        BASE_URL="http://localhost:5000",
        USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    if app.config["USE_NGROK"] and os.environ.get("NGROK_AUTHTOKEN"):
        # pyngrok will only be installed, and should only ever be initialized, in a dev environment
        from pyngrok import ngrok

        # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "5000"

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

        # Update any base URLs or webhooks to use the public ngrok URL
        app.config["BASE_URL"] = public_url
        init_webhooks(public_url)

    # ... Initialize Blueprints and the rest of our app
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(cyanite_blueprint, url_prefix='/cyanite')

    return app
