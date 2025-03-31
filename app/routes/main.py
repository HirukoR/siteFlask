from flask import Blueprint, render_template
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', current_year=datetime.now().year)

@main.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year} 