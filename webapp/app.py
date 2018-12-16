from flask import Flask, send_from_directory, make_response
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

    @app.route('/<path:path>')
    def serve_static(path):
        resp = make_response(send_from_directory(app.static_folder, path))
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    @app.route('/')
    def index_page():
        return send_from_directory(app.static_folder, 'login.html')

    return app

if __name__ == "__main__":
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    app = create_app(debug=debug)
    app.run(host='0.0.0.0')
