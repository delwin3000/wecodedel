from flask_login import UserMixin
from extensions import db

visited_songs = db.Table('visited_songs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    visited = db.relationship('Song', secondary=visited_songs, backref=db.backref('visitors', lazy='dynamic'))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Song {self.title} by {self.artist}>"

