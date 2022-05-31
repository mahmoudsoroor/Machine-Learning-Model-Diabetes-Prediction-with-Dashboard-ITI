from flask import Flask
from config import Config
import pickle



def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        
        from . import routes

        
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

        return app



rf_model = pickle.load(open('app/data/rf_model_pkl', 'rb'))

