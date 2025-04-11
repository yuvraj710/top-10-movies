from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from tmdb_api import search_movies, get_movie_details
import os

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Movie model
class Movie(db.Model):
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

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    selected_genre = request.args.get("genre")
    search_query = request.args.get("search")

    query = Movie.query

    if selected_genre and selected_genre != "All":
        query = query.filter(Movie.genres.ilike(f"%{selected_genre}%"))

    if search_query:
        query = query.filter(Movie.title.ilike(f"%{search_query}%"))

    all_movies = query.order_by(Movie.rating.desc()).all()

    for i, movie in enumerate(all_movies):
        movie.ranking = i + 1
    db.session.commit()

    # Build genre dropdown list
    genre_set = set()
    for movie in Movie.query.all():
        if movie.genres:
            genre_list = [g.strip() for g in movie.genres.split(",")]
            genre_set.update(genre_list)

    genre_list = sorted(genre_set)

    return render_template("index.html", movies=all_movies,
                           selected_genre=selected_genre,
                           search_query=search_query,
                           all_genres=genre_list)

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/find")
def find_movie():
    movie_title = request.args.get("title")
    if movie_title:
        movies = search_movies(movie_title)
        return render_template("select.html", movies=movies)
    return redirect(url_for("add"))

@app.route("/add/<int:tmdb_id>")
def add_movie(tmdb_id):
    movie_data = get_movie_details(tmdb_id)

    existing = Movie.query.filter_by(title=movie_data["title"]).first()
    if existing:
        return redirect(url_for("edit", movie_id=existing.id))

    new_movie = Movie(
        title=movie_data["title"],
        year=movie_data["release_date"].split("-")[0] if movie_data["release_date"] else "N/A",
        description=movie_data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get("poster_path") else "",
        trailer_url=movie_data.get("trailer_url"),
        genres=movie_data.get("genre_names")
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit", movie_id=new_movie.id))

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get(movie_id)
    if request.method == "POST":
        movie.rating = float(request.form["rating"])
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie)

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.template_filter("stars")
def stars_filter(rating):
    if rating is None:
        return ""
    rounded = round(rating / 2)
    stars_html = ""
    for i in range(5):
        if i < rounded:
            stars_html += '<i class="star full">★</i>'
        else:
            stars_html += '<i class="star empty">☆</i>'
    return stars_html

if __name__ == '__main__':
    app.run(debug=True)
