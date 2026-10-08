from flask import Flask, render_template, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if app.debug:

    @app.get('/api/docs/')
    def api_docs():
        return render_template('redoc.html')

    @app.get('/api/openapi.yml')
    def openapi_spec():
        return send_from_directory('..', 'openapi.yml')
