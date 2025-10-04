"""Dynamically create an HTML file for a list of animal objects."""
from data_fetcher import get_animals
from file_handling import write_html_file
from data_processing import get_skin_types
from animals_web_generator import serialize_all_animals_to_html

TEMPLATE_FILE = "animals_template.html"
NEW_FILE = "animals.html"


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
    elif animals_data is None:
        content = "<h2>There was a problem fetching the data from the API.</h2>"
    else:
        skin_type = ask_for_skin_type(animals_data)
        content = serialize_all_animals_to_html(animals_data, skin_type)
    write_html_file(TEMPLATE_FILE, NEW_FILE, content)
    print("Successfully generated the file 'animals.html'.")


if __name__ == "__main__":
    main()
