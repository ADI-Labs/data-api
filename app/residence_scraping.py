#!/usr/bin/env python
import os
from collections import defaultdict
from copy import copy
from robobrowser import RoboBrowser
from . import db
from .models import Residence
from .helpers import get_empty_json, upload_object_to_db

# URLs that are used to scrape.
BASE_URL = 'https://housing.columbia.edu'
HOME_URL = BASE_URL + '/compare-residences'

NON_STANDARD_RESIDENCES = {
    "FSL Brownstones",
    "Residential Brownstones",
    "SIC Residences"
}

CLASS_FOR_FIELD = {
    "description": "field-type-text-with-summary",
    "residential_area": "field-name-field-residence-programs",
    "building_type": "field-name-field-residence-building-type",
    "room_type": "field-name-field-residence-room-type",
    "class_make_up": "field-name-field-residence-class-make-up",
    "rate": "field-name-field-residence-rate",
    "entrance_info": "field-name-field-residence-entrance-info",
    "num_res_floors": "field-name-field-residence-number-of-floors",
    "singles_doubles": "field-name-field-residence-singles-doubles",
    # "batrhoom-fc" spelling is correct, as also in html
    "bathroom": "field-name-field-residence-batrhoom-fc",
    "laundry": "field-name-field-residence-laundry-fc",
    "flooring": "field-name-field-residence-flooring",
    "kitchen": "field-name-field-residence-kitchen-fc",
    "lounge": "field-name-field-residence-lounge-fc",
    "cleaning_schedule": "field-name-field-residence-cleaning-fc",
    "features": "field-name-field-residence-features",
    "bike_storage": "field-name-field-residence-bike-fc",
    "print_station": "field-name-field-residence-print-station-fc",
    "fitness_room": "field-name-field-residence-fitness-fc",
    "computer_lab": "field-name-field-residence-computer-fc",
    "ac": "field-name-field-residence-ac",
    "piano": "field-name-field-residence-piano-fc",
    "student_reviews": "field-name-field-residence-student-comments"
}

NON_STANDARDIZED_FIELDS = [
    "name",
    "street_address",
    "residential_area",
    "description",
    "rate",
    "entrance_info",
    "flooring",
    "features",
    "cleaning_schedule",
    "lounge",
    "_expand_category"
]

BOOLEAN_FIELDS = [
    "bike_storage",
    "print_station",
    "fitness_room",
    "computer_lab",
    "ac",
    "piano"
]


def get_residences():
    """
    Gets raw residence data from Columbia housing website, standardizes
    and cleans the data, and uploads to the database
    """
    browser = RoboBrowser()
    residences_list = []

    # makes list of links to each residence hall page
    browser.open(HOME_URL)
    table_headers = browser.find_all(class_='views-field-title')[1:]
    residence_links = list(map(lambda x: x.find('a')['href'], table_headers))

    for link in residence_links:
        browser.open(BASE_URL + link)
        residence_json = parse_residence_info(browser)
        residences_list.extend(residence_json)

    if not os.path.isfile('app/data.sqlite'):
        print("Creating database")
        db.create_all()

    # uncomment to see collected data
    # collate_data(residences_list)

    print("Uploading residences to database")
    for res in residences_list:
        upload_object_to_db(Residence, res)


# Parsing methods


def parse_residence_info(browser):
    """
    Parses residence objects from the data on the current browser page
    Returns a list of dictionaries of residence json for the current page

    params:
        browser: Robobrowser currently on residence page
    """

    new_res = get_empty_json(Residence)
    new_res["singles_doubles"] = ""
    del new_res["num_singles"]
    del new_res["num_doubles"]
    new_res["name"] = tag_text(browser.find(id="page-title"))
    print("Scraping info for", new_res["name"])

    for field in new_res:
        if field in CLASS_FOR_FIELD:
            new_res[field] = parse_tag(browser, CLASS_FOR_FIELD[field])

    # Parse residencee differently for special residence types
    if new_res["name"] in NON_STANDARD_RESIDENCES:
        residences = []

        # create residence json for grouped entry
        formatted_residence = standardize_residence(new_res)
        formatted_residence["_expand_category"] = "group"
        formatted_residence["street_address"] = "Varies"
        formatted_residence["building_type"] = "Special, " + \
            formatted_residence["building_type"]
        residences.append(formatted_residence)

        #  get address and name tuples for specific buildings under group
        expanded_residences = parse_non_standard_addresses(browser)

        # create expanded residence json for each specific building
        for res_name, res_add in expanded_residences:
            res = copy(formatted_residence)
            res["name"] = res_name
            res["street_address"] = res_add
            res["_expand_category"] = "expand"
            residences.append(res)

        return residences

    # Handle normal residences
    else:
        new_res["street_address"] = \
            tag_text(browser.find(class_="dotted-title"))

        for field in new_res:
            if field in CLASS_FOR_FIELD:
                new_res[field] = parse_tag(browser, CLASS_FOR_FIELD[field])

        # add _expand_category tag for standard residences
        new_res["_expand_category"] = "expand group"

        formatted_residence = standardize_residence(new_res)
        return [formatted_residence]


def standardize_residence(raw_json):
    """
    Standardizes the fields of a residence object
    Returns the standardized json object
    """
    db_entry = {}

    # copy over unchanged fields
    for field in NON_STANDARDIZED_FIELDS:
        db_entry[field] = raw_json[field] if raw_json[field] else "Unspecified"

    # set boolean fields
    for field in BOOLEAN_FIELDS:
        if raw_json[field]:
            negated = raw_json[field] == "No"
            db_entry[field] = False if negated else True
        else:
            db_entry[field] = False

    # class make up, set "First-Year" to "Freshmen"
    class_str = raw_json["class_make_up"].replace("First-Year", "Freshmen")
    db_entry["class_make_up"] = class_str

    # building type, options are suite, apartment, or corridor style
    if "suite" in raw_json["building_type"].lower():
        db_entry["building_type"] = "Suite-style"
    else:
        db_entry["building_type"] = raw_json["building_type"]
    if "townhouse" in raw_json["building_type"].lower():
        db_entry["building_type"] += ", Townhouses"

    # room type: singles/doubles, studio singles/doubles, suite
    # singles/doubles, walkthrough doubles, one/two bedrooms
    room_strs = raw_json["room_type"].split(", ")
    parsed_strs = []
    for s in room_strs:
        st = s.lower().replace("large ", "")
        if "walk-through" in st or "bedrooms" in st or "studio" in st:
            parsed_strs.append(st)
        elif "suite" in st:
            if "double" in st:
                parsed_strs.append("suite doubles")
            if "single" in st:
                parsed_strs.append("suite singles")
        elif "double" in st:
            parsed_strs.append("doubles")
        elif "single" in st:
            parsed_strs.append("singles")
    db_entry["room_type"] = ", ".join(parsed_strs)

    # num_res_floors, hard code missing values
    if db_entry["name"] == "Ruggles Hall":
        db_entry["num_res_floors"] = 8  # Ruggles has 8 floors
    # leave SIC Residences as null as it varies
    elif db_entry["name"] == "SIC Residences":
        pass
    elif raw_json["num_res_floors"]:
        db_entry["num_res_floors"] = extract_int(raw_json["num_res_floors"])

    # split singles/doubles into two entries
    if raw_json["singles_doubles"]:
        singles_doubles = raw_json["singles_doubles"].split("/")
        db_entry["num_singles"] = extract_int(singles_doubles[0])
        db_entry["num_doubles"] = extract_int(singles_doubles[1])

    # bathrooms, ensure all entries start with private,
    # semi-private, or shared
    db_entry["bathroom"] = raw_json["bathroom"]
    search_terms = [
        "Shared",
        "Private",
        "Semi-Private"
    ]
    if db_entry["bathroom"].split(", ")[0] not in search_terms:
        db_entry["bathroom"] = "Shared, " + db_entry["bathroom"]

    # laundry, location
    db_entry["laundry"] = raw_json["laundry"] \
        .replace(";", ",") \
        .replace(".", ",") \
        .split(', ')[1]

    # kitchen, hard code for John Jay
    if raw_json["kitchen"]:
        kitchen_details = raw_json["kitchen"].split(", ")
        if kitchen_details[0] == "Available":
            db_entry["kitchen"] = "Shared, per floor"
        else:
            db_entry["kitchen"] = kitchen_details[0]
            if "per floor" in kitchen_details[1].lower():
                db_entry["kitchen"] += ", per floor"
            elif "per suite" in kitchen_details[1].lower():
                db_entry["kitchen"] += ", per suite"
            elif "per apartment" in kitchen_details[1].lower():
                db_entry["kitchen"] += ", per apartment"
            else:
                db_entry["kitchen"] += ", " + kitchen_details[1]
    else:  # hard code John Jay
        db_entry["kitchen"] = "Not available"

    return db_entry


def parse_field_item(item_list):
    """
    Returns a list of strings from a field item
    """
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
    class_: name of css class for field
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


def parse_non_standard_addresses(browser):
    """
    Parses a list of name, address tuples from the current page
    """
    container = browser.find(class_="field-name-field-residence-address")
    rows = container.find_all("tr")

    residences_name_add = []
    for row in rows:
        segments = row.find_all("td")
        address = tag_text(segments[0])
        if "Address" in address or not address:
            continue
        names = segments[1].find_all("div")
        if len(names) > 0:
            for name_tag in names:
                name = tag_text(name_tag)
                if name == "West Campus":
                    name = address
                if name:
                    residences_name_add.append((name, address))
        else:
            lis = segments[1].find_all("li")
            if len(lis) > 0:
                for li in lis:
                    name = tag_text(li)
                    residences_name_add.append((name, address))
            else:
                name = tag_text(segments[1])
                if name == "West Campus":
                    name = address
                residences_name_add.append((name, address))

    return residences_name_add


# Helper methods


def extract_int(string):
    """
    Extracts just the integer from a string
    Assumes that there is exactly one integer included
    """
    return int("".join(list(filter(lambda x: x.isdigit(), string))))


def collate_data(res_list):
    """
    Collates data by field and prints to console
    """
    data_entries = defaultdict(list)
    for res in res_list:
        for field in res:
            data_entries[field].append(res[field])

    for field in data_entries:
        print("")
        print(field, ":")
        for entry in data_entries[field]:
            print("    ", entry)


def tag_text(tag):
    """
    Returns the text contained within a tag
    """
    text = tag.get_text()
    text = text \
        .replace("\n", "") \
        .replace("\u00a0", " ") \
        .replace("\u2019", "'") \
        .replace("\u201c", "\"") \
        .replace("\u201d", "\"") \
        .replace("\u2014", "-") \
        .replace("\u2013", "-") \
        .replace("\u2026", "...") \
        .replace("\"\"", "\", \"")
    if text[-2:] == ", ":
        text = text[:-2]

    return text.strip()
