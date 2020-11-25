import argparse

import flask

from api.prod.routes import api as prod_api
from api.stubs.routes import api as stub_api

def create_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Run test version with static responses.", action="store_true")
    args = parser.parse_args()

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    if args.test:
        app.register_blueprint(stub_api)
    else:
        app.register_blueprint(prod_api)
    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
