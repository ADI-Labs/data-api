#!/usr/bin/env python
import os
from collections import defaultdict
from robobrowser import RoboBrowser
from . import db
from .models import Residence
from .helpers import check_differences

# URLs that are used to scrape.
base_url = 'https://housing.columbia.edu'
home_url = base_url + '/compare-residences'


def get_residences():
    """
    Gets raw residence data from Columbia housing website, standardizes
    and cleans the data, and uploads to the database
    """
    browser = RoboBrowser()
    residences_list = []

    # makes list of links to each residence hall page
    browser.open(home_url)
    table_headers = browser.find_all(class_='views-field-title')[1:]
    residence_links = list(map(lambda x: x.find('a')['href'], table_headers))

    for link in residence_links:
        browser.open(base_url + link)
        residence_json = parse_residence_info(browser)
        if residence_json:
            residences_list.append(residence_json)

    if not os.path.isfile('app/data.sqlite'):
        print("Creating database")
        db.create_all()

    collate_data(residences_list)  # here just for data analysis
    print("Uploading residences to database")
    upload_residences_to_db(residences_list)


def parse_residence_info(browser):
    """
    Parses a residence object from the data on the current browser page
    Returns a dictionary of the residence json

    Parameters:
        browser: Robobrowser currently on residence page
    """

    new_res = get_new_residence()
    new_res["name"] = browser.find(id="page-title").get_text()
    print("Scraping info for", new_res["name"])

    # skip non-standard housing pages
    if new_res["name"] in [
        "FSL Brownstones",
        "Residential Brownstones",
        "SIC Residences"
    ]:
        print("Skipping", new_res["name"])
        return None

    new_res["street_address"] = tag_text(browser.find(class_="dotted-title"))

    class_for_fields = {
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

    for field in new_res:
        if field in class_for_fields:
            new_res[field] = parse_tag(browser, class_for_fields[field])

    formatted_residence = standardize_residence(new_res)
    return formatted_residence


# fields that don't require any modification / cleaning
# generally won't be searching by these (except name)
unchanged_fields = [
    "name",
    "street_address",
    "residential_area",
    "description",
    "rate",
    "entrance_info",
    "flooring",
    "features",
    "cleaning_schedule",
    "lounge"
]

boolean_fields = [
    "bike_storage",
    "print_station",
    "fitness_room",
    "computer_lab",
    "ac",
    "piano"
]


def standardize_residence(raw_json):
    db_entry = {}

    # copy over unchanged fields
    for field in unchanged_fields:
        db_entry[field] = raw_json[field] if raw_json[field] else "Unspecified"

    # set boolean fields
    for field in boolean_fields:
        if raw_json[field]:
            negated = raw_json[field] == "No"
            db_entry[field] = False if negated else True
        else:
            db_entry[field] = False

    # class make up, set "First-Year" to "Freshmen"
    class_str = raw_json["class_make_up"].replace("First-Year", "Freshmen")
    db_entry["class_make_up"] = class_str

    # building type, options are suite, apartement, or corridor style
    if "suite" in raw_json["building_type"].lower():
        db_entry["building_style"] = "Suite-style"
    else:
        db_entry["building_style"] = raw_json["building_type"]
    if "townhouse" in raw_json["building_type"].lower():
        db_entry["building_style"] += ", Townhouses"

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

    # num_res_floors missing from Ruggles, hard code value
    if raw_json["num_res_floors"]:
        db_entry["num_res_floors"] = extract_int(raw_json["num_res_floors"])
    else:
        db_entry["num_res_floors"] = 8  # Ruggles has 8 floors

    # split singles/doubles into two entries
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

    # laundry, location and if free
    # is_free = "free" in raw_json["laundry"]
    # db_entry["laundry"] = "Free, " if is_free else "Not free, "
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


def upload_residences_to_db(res_list):
    """
    Takes each residence from the list provided
    and either adds or updates its entry in the database

    Parameters:
        res_list: list of residence objects
    """
    for res in res_list:
        new_res = get_residence_from_dict(res)
        existing_res = Residence.query.get(new_res.name)
        if existing_res:
            # check for differences objects and then update
            existing_res = check_differences(existing_res, new_res)
        else:
            db.session.add(new_res)
    db.session.commit()


def get_new_residence():
    """
    Returns an empty residence dictionary
    Fields correspond to raw fields from housing website
    """
    return {
        "name": "",
        "street_address": "",
        "description": "",
        "residential_area": "",
        "building_type": "",
        "room_type": "",
        "class_make_up": "",
        "rate": "",
        "entrance_info": "",
        "num_res_floors": "",
        "singles_doubles": "",
        "bathroom": "",
        "laundry": "",
        "flooring": "",
        "kitchen": "",
        "lounge": "",
        "cleaning_schedule": "",
        "features": "",
        "bike_storage": "",
        "print_station": "",
        "fitness_room": "",
        "computer_lab": "",
        "ac": "",
        "piano": ""
    }


def get_residence_from_dict(res_dict):
    """
    Creates and returns a residence object

    Parameters:
        res_dict: dictionary with some or all of the required fields
    """
    return Residence(
        name=res_dict.get("name"),
        street_address=res_dict.get("street_address"),
        description=res_dict.get("description"),
        residential_area=res_dict.get("residential_area"),
        building_type=res_dict.get("building_type"),
        room_type=res_dict.get("room_type"),
        class_make_up=res_dict.get("class_make_up"),
        rate=res_dict.get("rate"),
        entrance_info=res_dict.get("entrance_info"),
        num_res_floors=res_dict.get("num_res_floors"),
        num_singles=res_dict.get("num_singles"),
        num_doubles=res_dict.get("num_doubles"),
        bathroom=res_dict.get("bathroom"),
        laundry=res_dict.get("laundry"),
        flooring=res_dict.get("flooring"),
        kitchen=res_dict.get("kitchen"),
        lounge=res_dict.get("lounge"),
        cleaning_schedule=res_dict.get("cleaning_schedule"),
        features=res_dict.get("features"),
        bike_storage=res_dict.get("bike_storage"),
        print_station=res_dict.get("print_station"),
        fitness_room=res_dict.get("fitness_room"),
        computer_lab=res_dict.get("computer_lab"),
        ac=res_dict.get("ac") or False,
        piano=res_dict.get("piano"),
    )


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
        .replace("\u201c", "\"") \
        .replace("\u201d", "\"") \
        .replace("\u2014", "-") \
        .replace("\u2013", "-") \
        .replace("\u2026", "...") \
        .replace("\"\"", "\", \"")
    if text[-2:] == ", ":
        text = text[:-2]

    return text


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
