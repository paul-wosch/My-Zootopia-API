"""Read HTML template and write new HTML file."""
PLACEHOLDER = "            __REPLACE_ANIMALS_INFO__"


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
