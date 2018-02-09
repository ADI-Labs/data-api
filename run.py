from app import create_app, db
from app.models import User


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)

@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(suite)
