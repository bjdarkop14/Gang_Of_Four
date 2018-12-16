from flask import Flask
from flask_cors import CORS

from app.view import main_view
import sys

def create_app(debug=False):
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main_view.user)
    app.register_blueprint(main_view.areas)
    app.register_blueprint(main_view.group)
    app.register_blueprint(main_view.chat)
    app.debug = debug

    return app

if __name__ == "__main__":
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    app = create_app(debug=debug)
    app.run(host='0.0.0.0')
