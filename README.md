# 🎬 Top 10 Movies Flask App

A clean, fully functional movie tracking web app built with **Flask**, **SQLAlchemy**, and the **TMDb API**. This project allows users to manage a top-10 movie list, view trailers, add reviews and ratings, filter by genre, and search by title — all powered by dynamic backend logic and a polished UI.

---

## 📦 Features

- ✅ Add movies using live search from the [TMDb API](https://www.themoviedb.org/)
- ✅ View full movie poster, title, release year, and description
- ✅ Assign ratings and reviews
- ✅ Auto-ranked top 10 list (by rating)
- ✅ Gold & gray star visuals for rating clarity
- ✅ View official movie trailers (YouTube)
- ✅ Filter by **genre** (dynamically extracted)
- ✅ Search by **movie title** (case-insensitive)
- ✅ Clear, responsive UI using **Bootstrap 5**

---

## 🛠️ Built With

- Python 3
- Flask
- SQLAlchemy (SQLite DB)
- Jinja2
- Bootstrap 5
- TMDb API (title, poster, year, trailer, genres)

---

## 🚀 Getting Started

### 🔧 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🧪 Run Locally
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

### 🗝️ TMDb API Key
1. Go to [TMDb Developers](https://developer.themoviedb.org/)
2. Create an account + request an API key
3. Create a `.env` file:
```
TMDB_API_KEY=your_tmdb_api_key_here
```

---

## 🧠 Code Structure
```
├── app.py                # Main Flask app
├── tmdb_api.py           # Handles all TMDb API calls
├── templates/
│   ├── index.html        # Homepage with movie grid
│   ├── add.html          # Form to search TMDb
│   ├── select.html       # Pick from TMDb results
│   └── edit.html         # Rate & review
├── static/
│   └── (optional styling)
├── requirements.txt
├── .env                  # Contains TMDB_API_KEY
└── README.md
```

---

## 💡 Project Status

This version is complete and serves as the **backend-focused showcase** with API integration, filtering, searching, and UI rendering.

✅ Use this as a base for:
- Deploying a frontend-optimized web app
- Adding user authentication (login, favorites)
- Using PostgreSQL or MongoDB for production
- Full-stack deployment (Render, Fly.io, etc.)

---
## 📄 License
MIT License — free for personal and commercial use.
