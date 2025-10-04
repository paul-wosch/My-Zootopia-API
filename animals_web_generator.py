"""Generate HTML file from API Ninjas Animals API for selected fields."""
from data_fetcher import get_animals
from data_processing import get_animal, get_skin_types
from file_handling import write_html_file

TEMPLATE_FILE = "animals_template.html"
NEW_FILE = "animals.html"
INDENTATION = "    "


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
            if animal["characteristics"].get("skin_type", "N/A") == skin_type:
                animal_obj = get_animal(animal)
                output += serialize_animal_to_html(animal_obj) + "\n"
    return output


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
    if not animals_data and isinstance(animals_data, list):
        content = f"<h2>The animal '{animal_name}' doesn\'t exist.</h2>"
    else:
        skin_type = ask_for_skin_type(animals_data)
        content = serialize_all_animals_to_html(animals_data, skin_type)
    write_html_file(TEMPLATE_FILE, NEW_FILE, content)
    print("Website was successfully generated to the file animals.html.")


if __name__ == "__main__":
    main()
