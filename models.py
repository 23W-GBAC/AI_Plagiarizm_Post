from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image_filename = db.Column(db.String(120), unique=True, nullable=False)
    comments = db.relationship('Comment', backref='artwork', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
