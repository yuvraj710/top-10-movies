"""
models.py – Database model definitions for the Top 10 Movies app.

Defines the SQLAlchemy database instance and Movie model.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance (init_app will be used in app.py)
db = SQLAlchemy()

class Movie(db.Model):
    """
    Movie model representing a single movie entry in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(4), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    trailer_url = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Movie {self.title} ({self.year}) – Rating: {self.rating}>"
