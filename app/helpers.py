from . import db


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


def check_differences(existing_item, new_item, persisted_hidden_attributes=[]):
    existing_data = remove_hidden_attr(existing_item.__dict__)
    new_data = remove_hidden_attr(new_item.__dict__)

    # allow for user set hidden attributes
    if len(persisted_hidden_attributes) > 0:
        for att in persisted_hidden_attributes:
            existing_data[att] = existing_item.__dict__[att]
            new_data[att] = new_item.__dict__[att]

    # for each parameter
    for key in existing_data.keys():
        # if there is a difference, set to new data
        if existing_data[key] != new_data.get(key):
            print(
                'updating ',
                existing_item,
                key,
                existing_data[key],
                '->',
                new_data.get(key))
            setattr(existing_item, key, new_data.get(key))

    db.session.flush()
