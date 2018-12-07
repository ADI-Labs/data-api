from app import create_app
from app.helpers import get_courses

app = create_app()

with app.app_context():
    get_courses()
