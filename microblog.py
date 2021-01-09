from app import app, db
from app.models import User, Nom, Contract

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Nominations': Nom, 'Contract': Contract}