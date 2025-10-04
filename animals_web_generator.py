"""Create the HTML code to show animals with some of their attributes
from a list of animal objects."""
from data_processing import get_animal

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
