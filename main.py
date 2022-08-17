from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from api_config import API_TOKEN
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# TODO--1a. Create a db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class RateMovieForm(FlaskForm):
    rating = StringField(label='Your Rating our of 10 e.g. 7.5')
    review = StringField(label='Your Review')
    submit = SubmitField(label='Submit')


class AddMovieForm(FlaskForm):
    title = StringField()
    submit = SubmitField(label='Add Movie')


# TODO--1b. Create table with pertinent data fields
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=True)
    year = db.Column(db.Integer, unique=False, nullable=True)
    description = db.Column(db.String(100), unique=False, nullable=True)
    rating = db.Column(db.Integer, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String, unique=False, nullable=True)
    img_url = db.Column(db.String, unique=False, nullable=True)


my_movies = Movie()
db.create_all()


if not my_movies.query.get(1):
    my_movies.title = 'Saturday Night Fever'
    my_movies.year = 1977
    my_movies.description = "Tony Manero (John Travolta) doesn't have much going for him during the weekdays. " \
                            "He still lives at home and works as a paint store clerk in his Brooklyn, N.Y., neighborhood. " \
                            "But he lives for the weekends, when he and his friends go to the local disco and dance the night away. " \

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
    all_movies = my_movies.query.order_by('rating')
    num_movies = my_movies.query.count()
    i = 0
    # Assign a ranking number to each movie
    for movie in all_movies:
        movie.ranking = num_movies - i
        i += 1

    return render_template("index.html", movies=all_movies)


@app.route('/edit.html', methods=['POST', 'GET'])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get('movie_id')
    movie = my_movies.query.get(movie_id)

    if request.method == 'GET':
        if request.args.get('movie_title'):
            movie_title = request.args.get('movie_title')

            deleted_movie = my_movies.query.filter_by(title=movie_title).first()
            db.session.delete(deleted_movie)
            db.session.commit()
            return redirect('/')
        return render_template('edit.html', form=form, movie=movie)

    # This isn't activated until user clicks submit
    elif request.method == 'POST':
        new_rating = request.form['rating']
        new_review = request.form['review']

        movie.rating = new_rating
        movie.review = new_review
        db.session.commit()
        return redirect('/')


@app.route('/add.html', methods=['POST', 'GET'])
def add():
    # TODO--7. Implement add functionality
    add_movie_form = AddMovieForm()

    # If user clicks 'add movie' button
    if request.method == 'POST':
        my_movies.title = request.form['title']
        # Check if movie exists, if so, redirect home
        if my_movies.query.filter_by(title=request.form['title']).first():
            print(f'{my_movies.title} not added:it already exists!')
            return redirect('/')
        else:
            # Search the tmdb for title
            endpoint = f'https://api.themoviedb.org/3/search/movie/'
            headers = {
                'Authorization': f'Bearer {API_TOKEN}',
                'Content-Type': 'application/json; charset=utf-8'
            }

            params = {
                'query': f'{my_movies.title}'
            }
            # Show tmdb results
            r = requests.get(url=endpoint, headers=headers, params=params)
            search_results = r.json()['results']
            return render_template('select.html', results=search_results)

    # If movie id is passed, search for it and add to db
    if request.args.get('movie_id'):
        movie_id = request.args.get('movie_id')
        search_endpoint = f'https://api.themoviedb.org/3/movie/{movie_id}'
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        r = requests.get(url=search_endpoint, headers=headers)
        movie = r.json()

        # Extract all movie data
        title = movie['original_title']
        movie_year = movie['release_date']
        description = movie['overview']
        img_url = movie['poster_path']

        # Use just the year for the movie
        dt = datetime.strptime(movie_year, '%Y-%m-%d')
        year = dt.year

        # Create new record and add to db
        new_movie = Movie()
        new_movie.title = title
        new_movie.year = year
        new_movie.img_url = 'https://image.tmdb.org/t/p/original/' + img_url
        new_movie.description = description

        db.session.add(new_movie)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=add_movie_form)


if __name__ == '__main__':
    app.run(debug=True)
