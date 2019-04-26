from app import create_app
from app.courses_scraping import get_courses

app = create_app()

with app.app_context():
    get_courses()
