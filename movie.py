"""
This is the direktor module and supports all the REST actions for the
movie data
"""

from flask import make_response, abort
from config import db
from models import Director, MovieSchema, Movie
import math

def read_all():
    """
    This function responds to a request for /api/movie
    with the complete lists of movie

    :return:        json string of list of movie
    """
    # Create the list of people from our data
    movies = Movie.query.order_by(Movie.title).limit(50)

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_all_pagination(page,per_page):
    """
    This function responds to a request for /api/movie
    with the complete lists of movie  with pagination

    :param page:          page of current view page
    :param per_page:      how much data to view in one page
    :return:        json string of list of movie
    """
    # Create the list of people from our data
    movies = Movie.query.order_by(Movie.title).paginate(page,per_page).items

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)

    # for get length of query data
    n =len(Movie.query.all())

    # get max page to return to View
    max_page = math.ceil(n/per_page)
    
    #append to data list for response to view
    mp = {
        'Max_Page': max_page
    }
    data.append(mp)
    return data

def read_one(director_id,movie_id):
    """
    This function responds to a request for /api/movie/{movie_id}
    with one matching movie

    :param movie_id:   Id of movie to find
    :return:            movie matching id
    """
    # Build the initial query
    movies = (
        Movie.query.join(Director,Director.id == Movie.director_id)
        .filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # Did we find a movie?
    if movies is not None:

        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movies)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def create(director_id,movie):
    """
    This function creates a new movie related to the passed in director id.

    :param director_id:     Id of the director the movie is related to
    :param movie:           The JSON containing the movie data
    :return:                201 on success
    """

    # get the parent person director
    person = Director.query.filter(Director.id == director_id).one_or_none()

    # Was a person found?
    if person is None:
        abort(404, f"Person not found for Director Id: {director_id}")

    # Create a movie schema instance
    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the movie to the person director and database
    person.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)

    return data, 201


def update(director_id, movie_id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.

    :param director_id:     Id of the director the movie is related to
    :param movie_id:        Id of the movie to update
    :param movie:           The JSON containing the movie data
    :return:                200 on success
    """
    update_movie = (
        Movie.query.filter(Movie.director_id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # Did we find an existing movie?
    if update_movie is not None:

        # turn the passed in movie into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id's to the movie we want to update
        update.director_id = update_movie.director_id
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def delete(director_id, movie_id):
    """
    This function deletes a movie from the movie structure

    :param director_id:  Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movie = (
        Movie.query.filter(Movie.director_id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted".format(movie_id=movie_id), 200
        )

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")