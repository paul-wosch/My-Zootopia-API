"""Generate HTML file from API Ninjas Animals API for selected fields."""
from data_fetcher import get_animals

TEMPLATE_FILE = "animals_template.html"
NEW_FILE = "animals.html"
PLACEHOLDER = "            __REPLACE_ANIMALS_INFO__"
INDENTATION = "    "
# Choose here, which fields to display beside animal name from JSON data.
# Usage: {<field name to display>: (<node>, <nested node>), ...}
SELECTED_FIELDS = {"diet": ("characteristics", "diet"),
                   "locations": ("locations",),
                   "type": ("characteristics", "type"),
                   "scientific name": ("taxonomy", "scientific_name"),
                   "skin type": ("characteristics", "skin_type")
                   }

# TODO: move animal object related function to animal_object.py
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

# TODO: remove unused function
def get_formated_animal(animal_obj):
    """Return formatted animal basics."""
    output = "\n".join(f"{key.title()}: {value}"
                       for key, value
                       in animal_obj.items()
                       if value)
    return output


def indent(n):
    """Return n indentations."""
    return INDENTATION * n


def serialize_animal_to_html(animal_obj):
    """Return animal information serialized as HTML."""
    output = ''
    output += f'{indent(3)}<li class="cards__item">'
    output += f'\n{indent(4)}<div class="card__title">{animal_obj["name"]}</div>'
    output += f'\n{indent(4)}<div class="card__text">'
    output += f'\n{indent(5)}<ul class="cards">'
    output += f'\n{indent(6)}'
    output += f'\n{indent(6)}'.join(f'<li><strong>{key.title()}:</strong> {value}</li>'
                                    for key, value
                                    in animal_obj.items()
                                    if not key == "name" and value)
    output += f'\n{indent(5)}</ul>'
    output += f'\n{indent(4)}</div>'
    output += f'\n{indent(3)}</li>'

    return output


def serialize_all_animals_to_html(animals, skin_type):
    """Return basic information for each animal
    for the given json animal data serialized as HTML."""
    output = ""
    if not skin_type:
        for animal in animals:
            animal_obj = get_animal(animal)
            output += serialize_animal_to_html(animal_obj) + "\n"
    else:
        for animal in animals:
            if animal["characteristics"]["skin_type"] == skin_type:
                animal_obj = get_animal(animal)
                output += serialize_animal_to_html(animal_obj) + "\n"
    return output

# TODO: move file related functions to 'file_handling.py'
def load_template(template_file):
    """Load and return html template."""
    with open(template_file, "r", encoding="utf-8") as file_obj:
        html_template = file_obj.read()
    return html_template


def write_file(file_name, content):
    """Write a file with the given content."""
    with open(file_name, "w", encoding="utf-8") as file_obj:
        file_obj.write(content)


def write_html_file(template_file, new_file, content):
    """Write a new html file for the given content."""
    html_template = load_template(template_file)
    html_new = html_template.replace(PLACEHOLDER, content)
    write_file(new_file, html_new)


def get_skin_types(animals):
    """Return a set of all skin types from the given JSON animal data."""
    # TODO: add fallback for missing key "skin_type"
    return set(animal["characteristics"]["skin_type"] for animal in animals)


def ask_for_animal_name() -> str:
    """Ask the user to enter the animal name to look for
    and return this value.
    """
    while True:
        animal_name = input("Enter a name of an animal: ").strip()
        if animal_name:
            break
        print("Input should not be empty.")
    return animal_name


def ask_for_skin_type(animals):
    """Ask the user to filter the list for a specific skin type."""
    print("Include only animals with the selected skin type.")
    skin_types = get_skin_types(animals)
    skin_types_str = ", ".join(f"'{skin_type}'" for skin_type in skin_types)
    while True:
        skin_type = input(f"Enter {skin_types_str} or leave empty for "
                          f"no filtering: ").strip().title()
        if skin_type in skin_types or skin_type == "":
            break
        print("Invalid skin type.")
    return skin_type


def main():
    """Ask for skin filter and generate HTML file."""
    animal_name = ask_for_animal_name()
    animals_data = get_animals(animal_name)
    print(animals_data)
    if not animals_data and isinstance(animals_data, list):
        content = f"<h2>The animal '{animal_name}' doesn\'t exist.</h2>"
    else:
        skin_type = ask_for_skin_type(animals_data)
        content = serialize_all_animals_to_html(animals_data, skin_type)
    write_html_file(TEMPLATE_FILE, NEW_FILE, content)
    print("Website was successfully generated to the file animals.html.")


if __name__ == "__main__":
    main()
