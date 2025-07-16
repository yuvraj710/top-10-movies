from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from tmdb_api import search_movies, get_movie_details
from models import db, Movie
from forms import EditForm
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "fallback-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

    genre_set = set()
    for movie in Movie.query.all():
        if movie.genres:
            genre_list = [g.strip() for g in movie.genres.split(",")]
            genre_set.update(genre_list)

    return render_template("index.html",
                           movies=all_movies,
                           selected_genre=selected_genre,
                           search_query=search_query,
                           all_genres=sorted(genre_set))

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/find")
def find_movie():
    movie_title = request.args.get("title")
    if not movie_title:
        return redirect(url_for("add"))

    try:
        movies = search_movies(movie_title)
    except Exception as e:
        logging.error(f"Error searching movies: {e}")
        return redirect(url_for("add"))

    return render_template("select.html", movies=movies)

@app.route("/add/<int:tmdb_id>")
def add_movie(tmdb_id):
    try:
        movie_data = get_movie_details(tmdb_id)
    except Exception as e:
        logging.error(f"Failed to fetch movie details: {e}")
        return redirect(url_for("add"))

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
    movie = Movie.query.get_or_404(movie_id)
    form = EditForm(obj=movie)

    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.template_filter("stars")
def stars_filter(rating):
    if rating is None:
        return ""
    rounded = round(rating / 2)
    return "".join(
        '<i class="star full">★</i>' if i < rounded else '<i class="star empty">☆</i>'
        for i in range(5)
    )

if __name__ == "__main__":
    app.run(debug=True)
