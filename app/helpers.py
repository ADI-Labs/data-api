from . import db
from .models import *
import os


def get_empty_json(model):
    """
    Returns a dictionary with keys for each of the columns of the model
    Each key is mapped to an empty string

    params:
        model: the database model in models.py to get the columns for
    """
    return {i: "" for i in get_column_names(model)}


def upload_object_to_db(model, obj_dict):
    """
    Adds or updates an object of type 'model' in the database
    Assumed keys in obj_dict correspond exactly to columns of model

    params:
        model: the database model in models.py that obj_dict corresponds to
        obj_dict: a dictionary of the field values for the object
    """
    if not os.path.isfile('app/data.sqlite'):
        db.create_all()
    sanitized_dict = {i: obj_dict.get(i) for i in get_column_names(model)}
    new_object = model(**sanitized_dict)
    identifiers = get_primary_keys(model, new_object)
    existing_object = model.query.get(tuple(identifiers))

    if existing_object:
        # check for differences objects and then update
        existing_object = check_and_update_differences(
            model,
            existing_object,
            new_object
        )
    else:
        db.session.add(new_object)
    db.session.commit()


def check_and_update_differences(model, existing_object, new_object):
    """
    Checks for and prints any updates fields on the object
    Returns the updated object
    """
    existing_data = {}
    new_data = {}

    # allow for user set hidden attributes
    for col in get_column_names(model):
        if not new_data.get(col):
            existing_data[col] = existing_object.__dict__[col]
            new_data[col] = new_object.__dict__[col]

    # for each parameter
    for key in existing_data.keys():
        # if there is a difference, set to new data
        if existing_data[key] != new_data.get(key):
            print(
                'updating ',
                existing_object,
                key,
                ' from ',
                existing_data[key],
                '->',
                new_data.get(key))
            setattr(existing_object, key, new_data.get(key))

    db.session.flush()
