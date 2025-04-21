from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

from models import Song

@main.route('/dashboard')
@login_required
def dashboard():
    songs = Song.query.all()
    return render_template('favourites.html', songs=songs)
