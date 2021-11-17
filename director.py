"""
This is the direktor module and supports all the REST actions for the
direktor data
"""

from operator import ge
from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie
import math


def read_all():
    """
    This function responds to a request for /api/director
    with the complete lists of director

    :return:        json string of list of director
    """
    # Create the list of people from our data
    director = Director.query.order_by(Director.name).limit(50)

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def read_all_pagination(page,per_page):
    """
    This function responds to a request for /api/director
    with the complete lists of director with pagination

    :param page:          page of current view page
    :param per_page:      how much data to view in one page
    :return:              json string of list of director with pagination and max page
    """
    # Create the list of people from our data
    director = Director.query.order_by(Director.name).paginate(page,per_page).items

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)

    # for get length of query data
    n =len(Director.query.all())

    # get max page to return to View
    max_page = math.ceil(n/per_page)

    #append to data list for response to view
    mp = {
        'Max_Page': max_page
    }
    data.append(mp)
    
    return data

def read_one(director_id):
    """
    This function responds to a request for /api/director/{director_id}
    with one matching person from director

    :param director_id:   Id of director to find
    :return:            director matching id
    """
    # Build the initial query
    person = (
        Director.query.filter(Director.id == director_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = DirectorSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {director_id}")

def read_all_filter_by_gender(gender):
    """
    This function responds to a request for /api/director
    with the complete lists of director

    :return:        json string of list of director
    """
    # Create the list of people from our data
    director = Director.query.filter(Director.gender == gender).order_by(Director.name).limit(50)

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def create(person):
    """
    This function creates a new person in the director structure
    based on the passed in director data

    :param person:  person to create in director structure
    :return:        201 on success, 406 on person exists
    """
    nama = person.get("name")
    uid = person.get("uid")

    existing_person = (
        Director.query.filter(Director.uid == uid)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_person is None:

        # Create a person instance using the schema and the passed in person
        schema = DirectorSchema()
        new_person = schema.load(person, session=db.session)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Person with UID {uid} exists already")


def update(director_id, person):
    """
    This function updates an existing person in the director structure

    :param director_id:   Id of the person to update in the director structure
    :param person:      person to update
    :return:            updated director structure
    """
    # Get the person requested from the db into session
    update_person = Director.query.filter(
        Director.id == director_id
    ).one_or_none()

    # Did we find an existing person?
    if update_person is not None:

        # turn the passed in person into a db object
        schema = DirectorSchema()
        update = schema.load(person, session=db.session)

        # Set the id to the person we want to update
        update.id = update_person.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person)

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {director_id}")


def delete(director_id):
    """
    This function deletes a person from the director structure

    :param director_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Director.query.filter(Director.id == director_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(f"Person {director_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {director_id}")

