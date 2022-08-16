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


class RateMovieForm(FlaskForm):
    rating = StringField(label='Your Rating our of 10 e.g. 7.5')
    review = StringField(label='Your Review')
    submit = SubmitField(label='Submit')


class AddMovieForm(FlaskForm):
    title = StringField()
    # year = StringField()
    # description = StringField()
    # rating = StringField()
    # ranking = StringField()
    # review = StringField()
    # img_url = StringField()
    submit = SubmitField(label='Add Movie')


# TODO--1b. Create table with pertinent data fields
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)
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

    if request.method == 'POST':
        my_movies.title = request.form['title']
        # my_movies.year = request.form['year']
        # my_movies.description = request.form['description']
        # my_movies.rating = request.form['description']
        # my_movies.ranking = request.form['ranking']
        # my_movies.review = request.form['review']
        # my_movies.img_url = request.form['img_url']
        # Check if movie already exists!
        if my_movies.query.filter_by(title=request.form['title']).first():
            print(f'{my_movies.title} not added:it already exists!')
            return redirect('/')
        else:
            db.session.add(my_movies)
            db.session.commit()
            return redirect('/')
    return render_template('add.html', form=add_movie_form)


if __name__ == '__main__':
    app.run(debug=True)
