# data_processing.py
# Choose here, which fields to display beside animal name from JSON data.
# Usage: {<field name to display>: (<node>, <nested node>), ...}
SELECTED_FIELDS = {"diet": ("characteristics", "diet"),
                   "locations": ("locations",),
                   "type": ("characteristics", "type"),
                   "scientific name": ("taxonomy", "scientific_name"),
                   "skin type": ("characteristics", "skin_type")
                   }


def initialize_animal_obj():
    """Initialize and return preprocessed animal object."""
    animal_obj = {}
    for field in SELECTED_FIELDS:
        animal_obj[field] = ""
    return animal_obj


def populate_animal_obj(animal):
    """Return populated animal object."""
    animal_obj = initialize_animal_obj()
    keys = list(animal_obj.keys())
    animal_obj["name"] = animal["name"]
    # dispatch key names to JSON nodes
    for key in keys:
        # treat special case where value is a list like in 'locations'
        if len(SELECTED_FIELDS[key]) > 1:
            animal_obj[key] = animal[SELECTED_FIELDS[key][0]].get(SELECTED_FIELDS[key][1], "")
        else:
            animal_obj[key] = ", ".join(animal[SELECTED_FIELDS[key][0]])
    return animal_obj


def get_animal(animal):
    """Return name and details for a given animal."""
    animal_obj = populate_animal_obj(animal)
    return animal_obj


def get_skin_types(animals) -> list:
    """Return all skin types from the given JSON animal data."""
    skin_types = set(animal["characteristics"].get("skin_type", "N/A") for animal in animals)
    skin_types_sorted = sorted(skin_types)
    return skin_types_sorted
