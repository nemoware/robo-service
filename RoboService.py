import argparse
import logging
from multiprocessing.pool import Pool

import flask

from api import doc_loader
from api.prod.routes import api as prod_api
from api.stubs.routes import api as stub_api

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


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
    doc_loader.pool = Pool(processes=1)
    try:
        create_app().run(host='0.0.0.0')
    except KeyboardInterrupt:
        doc_loader.pool.close()
        doc_loader.pool.join()
