from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# TODO--1a. Create a db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


# TODO--1b. Create table with pertinent data fields
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=False)
    review = db.Column(db.String, unique=False, nullable=False)
    img_url = db.Column(db.String, unique=False, nullable=False)


my_movies = Movie()
db.create_all()

if not my_movies.query.get(1):
    my_movies.title = 'Saturday Night Fever'
    my_movies.year = 1977
    my_movies.description = "Tony Manero (John Travolta) doesn't have much going for him during the weekdays. " \
                            "He still lives at home and works as a paint store clerk in his Brooklyn, N.Y., neighborhood. " \
                            "But he lives for the weekends, when he and his friends go to the local disco and dance the night away. " \
                            "When a big dance competition is announced, he wrangles the beautiful and talented Stephanie (Karen Lynn Gorney) to be his partner. " \
                            "As the two train for the big night, they start to fall for each other as well."
    my_movies.rating = 9.1
    my_movies.ranking = 1
    my_movies.review = "During my the 15 years I taught Latin dance, " \
                       "this was by far the movie I could most identify with."
    my_movies.img_url = "https://www.themoviedb.org/t/p/original/hbDQjNfOTglZBWv7WZqxpESXxXs.jpg"

    db.session.add(my_movies)
    db.session.commit()

# TODO 3a. Display image on front of card
@app.route("/")
def home():
    all_movies = my_movies.query.all()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
