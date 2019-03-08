#!/usr/bin/env python
import json
import os
import string
from robobrowser import RoboBrowser
from . import db
from .models import Residence
from .helpers import check_differences

# URLs that are used to scrape.
base_url = 'https://housing.columbia.edu'
home_url = base_url + '/compare-residences'
FILEPATH = './data/residence_data.json'


def get_residences():
    """
    Gets raw residence data from Columbia housing website, creates
    a json file and uploads to the database
    """
    global FILEPATH
    browser = RoboBrowser()
    residences_json_file = open(FILEPATH, 'wb+')

    # makes list of links to each residence hall page
    browser.open(home_url)
    table_headers = browser.find_all(class_='views-field-title')[1:]
    residence_links = list(map(lambda x: x.find('a')['href'], table_headers))

    for link in residence_links:
        browser.open(base_url + link)
        residence_json = parse_residence_info(browser)
        if residence_json:
            append_to_json_file(residence_json, residences_json_file)

    if not os.path.isfile('app/data.sqlite'):
        db.create_all()
    # upload_residences_to_db_from_file(FILEPATH)
    residences_json_file.close()


def parse_residence_info(browser):
    """
    Parses a residence object from the data on the current browser page
    Returns a dictionary of the residence json

    Parameters:
        browser: Robobrowser currently on residence page
    """

    new_res = get_new_residence()
    new_res["name"] = browser.find(id="page-title").get_text()

    print(new_res["name"])
    # skip non-standard housing pages
    if new_res["name"] in [
        "FSL Brownstones",
        "Residential Brownstones",
        "SIC Residences"
    ]:
        return None
    new_res["street_address"] = tag_text(browser.find(class_="dotted-title"))

    description_parent = browser.find(class_="field-type-text-with-summary")
    if description_parent.div.div.p:
        new_res["description"] = tag_text(description_parent.div.div.p)
    else:
        for line in description_parent.div.div.ul.children:
            text = tag_text(line)
            if text:
                new_res["description"] += text + ". "

    residential_area_class = "field-name-field-residence-programs"
    new_res["residential_area"] = parse_tag(browser, residential_area_class)

    building_type_class = "field-name-field-residence-building-type"
    new_res["building_type"] = parse_tag(browser, building_type_class)

    room_type_class = "field-name-field-residence-room-type"
    new_res["room_type"] = parse_tag(browser, room_type_class)

    class_make_up_class = "field-name-field-residence-class-make-up"
    new_res["class_make_up"] = parse_tag(browser, class_make_up_class)

    rate_class = "field-name-field-residence-rate"
    new_res["rate"] = parse_tag(browser, rate_class)

    entrance_info_class = "field-name-field-residence-entrance-info"
    new_res["entrance_info"] = parse_tag(browser, entrance_info_class)

    num_res_floors_class = "field-name-field-residence-number-of-floors"
    floors_str = parse_tag(browser, num_res_floors_class)
    if floors_str:
        new_res["num_res_floors"] = int(floors_str)

    singles_doubles_class = "field-name-field-residence-singles-doubles"
    new_res["singles_doubles"] = parse_tag(browser, singles_doubles_class)

    bathroom_class = "field-name-field-residence-batrhoom-fc"
    new_res["bathroom"] = parse_tag(browser, bathroom_class)

    laundry_class = "field-name-field-residence-laundry-fc"
    new_res["laundry"] = parse_tag(browser, laundry_class)

    flooring_class = "field-name-field-residence-flooring"
    new_res["flooring"] = parse_tag(browser, flooring_class)

    kitchen_class = "field-name-field-residence-kitchen-fc"
    new_res["kitchen"] = parse_tag(browser, kitchen_class)

    lounge_class = "field-name-field-residence-lounge-fc"
    new_res["lounge"] = parse_tag(browser, lounge_class)

    cleaning_schedule_class = "field-name-field-residence-cleaning-fc"
    new_res["cleaning_schedule"] = parse_tag(browser, cleaning_schedule_class)

    bike_storage_class = "field-name-field-residence-bike-fc"
    new_res["bike_storage"] = parse_tag(browser, bike_storage_class)

    print_station_class = "field-name-field-residence-print-station-fc"
    new_res["print_station"] = parse_tag(browser, print_station_class)

    fitness_room_class = "field-name-field-residence-fitness-fc"
    new_res["fitness_room"] = parse_tag(browser, fitness_room_class)

    computer_lab_class = "field-name-field-residence-computer-fc"
    new_res["computer_lab"] = parse_tag(browser, computer_lab_class)

    ac_class = "field-name-field-residence-ac"
    new_res["ac"] = parse_tag(browser, ac_class)

    piano_class = "field-name-field-residence-piano-fc"
    new_res["piano"] = parse_tag(browser, piano_class)

    student_reviews_class = "field-name-field-residence-student-comments"
    new_res["student_reviews"] = parse_tag(browser, student_reviews_class)

    features_class = "field-name-field-residence-features"
    new_res["features"] = parse_tag(browser, features_class)
    return new_res


def append_to_json_file(res_dict, json_file):
    """
    Appends a dict to a specific json file as a json object

    Parameters:
        dict: dictionary for JSON object
        json_file: file object to append to
    """

    # Checks if file has contents, appends if so
    json_file.seek(0, 2)
    if json_file.tell() == 0:
        json_file.write(json.dumps([res_dict], indent=4).encode())

    else:
        json_file.seek(-1, 2)
        json_file.truncate()
        json_file.write(' , '.encode())
        json_file.write(json.dumps(res_dict, indent=4).encode())
        json_file.write(']'.encode())


def upload_residences_to_db_from_file(filepath):
    """
    Takes each residence from the json file
    and either adds or updates its entry in the database

    Parameters:
        filepath: path to json file of residences
    """
    residences = json.load(open(filepath))
    for res in residences:
        new_res = get_residence_from_dict(res)
        existing_res = Residence.query.get(new_res.name)
        if existing_res:
            # check for differences objects and then update
            existing_res = check_differences(existing_res, new_res)
        else:
            db.session.add(new_res)
    db.session.commit()


def get_new_residence(res_dict={}):
    """
    Returns an empty residence object

    Parameters:
        res_dict: optional dictionary to initialize already know parameters
    """
    return {
        "name": res_dict.get("name") or "",
        "street_address": res_dict.get("street_address") or "",
        "description": res_dict.get("description") or "",
        "residential_area": res_dict.get("residential_area") or "",
        "building_type": res_dict.get("building_type") or "",
        "room_type": res_dict.get("room_type") or "",
        "class_make_up": res_dict.get("class_make_up") or "",
        "rate": res_dict.get("rate") or "",
        "entrance_info": res_dict.get("entrance_info") or "",
        "num_res_floors": res_dict.get("num_res_floors") or 0,
        "singles_doubles": res_dict.get("singles_doubles") or "",
        "bathroom": res_dict.get("bathroom") or "",
        "laundry": res_dict.get("laundry") or "",
        "flooring": res_dict.get("flooring") or "",
        "kitchen": res_dict.get("kitchen") or "",
        "lounge": res_dict.get("lounge") or "",
        "cleaning_schedule": res_dict.get("cleaning_schedule") or "",
        "features": res_dict.get("features") or "",
        # nullable below this point
        "bike_storage": res_dict.get("bike_storage") or "",
        "print_station": res_dict.get("print_station") or "",
        "fitness_room": res_dict.get("fitness_room") or "",
        "computer_lab": res_dict.get("computer_lab") or "",
        "ac": res_dict.get("ac") or False,
        "piano": res_dict.get("piano") or "",
        "student_reviews": res_dict.get("student_reviews") or ""
    }


def get_residence_from_dict(res_dict):
    """
    Creates and returns a residence object

    Parameters:
        res_dict: dictionary with some or all of the required fields
    """
    return Residence(
        name=res_dict.get("name") or "",
        street_address=res_dict.get("street_address") or "",
        description=res_dict.get("description") or "",
        residential_area=res_dict.get("residential_area") or "",
        building_type=res_dict.get("building_type") or "",
        room_type=res_dict.get("room_type") or "",
        class_make_up=res_dict.get("class_make_up") or "",
        rate=res_dict.get("rate") or "",
        entrance_info=res_dict.get("entrance_info") or "",
        num_res_floors=res_dict.get("num_res_floors") or 0,
        singles_doubles=res_dict.get("singles_doubles") or "",
        bathroom=res_dict.get("bathroom") or "",
        laundry=res_dict.get("laundry") or "",
        flooring=res_dict.get("flooring") or "",
        kitchen=res_dict.get("kitchen") or "",
        lounge=res_dict.get("lounge") or "",
        cleaning_schedule=res_dict.get("cleaning_schedule") or "",
        features=res_dict.get("features") or "",
        # nullable below this point
        bike_storage=res_dict.get("bike_storage") or "",
        print_station=res_dict.get("print_station") or "",
        fitness_room=res_dict.get("fitness_room") or "",
        computer_lab=res_dict.get("computer_lab") or "",
        ac=res_dict.get("ac") or False,
        piano=res_dict.get("piano") or "",
        student_reviews=res_dict.get("student_reviews") or ""
    )


printable = set(string.printable)


def tag_text(tag):
    """
    Returns the text contained within a tag

    Parameters:
        tag: beautifulsoup tag
    """
    text = tag.get_text()
    text = text.replace("\n", "") \
        .replace("\u00a0", " ") \
        .replace("\u2019", "'") \
        .replace(", ", "")
    text = "".join(list(filter(lambda x: x in printable, text)))

    return text


def parse_field_item(item_list):
    field_details = []
    items = item_list.find_all(class_="field-item")
    for item in items:
        ul = item.find("ul")
        if ul:
            lis = ul.find_all("li")
            for li in lis:
                text = tag_text(li)
                if text:
                    field_details.append(text)
        else:
            text = tag_text(item)
            if text:
                field_details.append(text)
    return field_details


def parse_tag(browser, class_):
    """
    Parses and returns a database field from the provided tag

    Parameters:
        class_: name of class to search for
    """
    class_tag = browser.find(class_=class_)
    if not class_tag:
        return ""

    field_details = []
    item_lists = class_tag.find_all(class_="field-items")
    if len(item_lists) > 1:
        for item_list in item_lists[1:]:
            field_details.extend(parse_field_item(item_list))
    elif len(item_lists) == 1:
        field_details.extend(parse_field_item(item_lists[0]))

    return ", ".join(field_details)
