from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Song
from app import db
from genius_api import search_songs, get_song_lyrics

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        flash("Invalid credentials")
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/song/<int:song_id>')
@login_required
def song_detail(song_id):
    try:
        song = Song.query.get_or_404(song_id)
        if song not in current_user.visited:
            current_user.visited.append(song)
            db.session.commit()
        if not song.lyrics:
            lyrics = get_song_lyrics(song.url)
            if lyrics:
                song.lyrics = lyrics
                db.session.commit()
        return render_template('song.html', song=song)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@auth.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    try:
        query = request.args.get('q', '')
        results = []
        if query:
            results = search_songs(query)
            # Save songs to DB if not exist
            for item in results:
                song = Song.query.filter_by(id=item['id']).first()
                if not song:
                    song = Song(id=item['id'], title=item['title'], artist=item['artist'], url=item['url'])
                    db.session.add(song)
            db.session.commit()
        return render_template('search.html', results=results, query=query)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@auth.route('/logs')
@login_required
def logs():
    try:
        import os
        log_path = os.path.join(os.getcwd(), 'logs', 'app.log')
        with open(log_path, 'r') as f:
            log_lines = f.readlines()
        # Show last 100 lines for performance
        log_lines = log_lines[-100:]
        return render_template('logs.html', logs=log_lines)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        app_logger = current_app.logger
        app_logger.error(f"Error reading logs: {error_details}")
        return f"An error occurred while reading logs: {str(e)}", 500
