import json
import os


# --- 1. File Handling Functions ---

def load_data(file_path):
    """
    Loads a JSON file with robust error handling for file I/O and JSON decoding.
    Returns the data structure on success, or None on failure.
    """
    if not os.path.exists(file_path):
        print(f"ERROR: File not found at path: {file_path}")
        return None

    try:
        with open(file_path, "r", encoding='utf-8') as handle:
            data = json.load(handle)
            return data
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from {file_path}. Details: {e}")
        return None
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while reading {file_path}. Details: {e}")
        return None


def read_template(file_path):
    """ Reads the content of an HTML template file. """
    with open(file_path, "r", encoding='utf-8') as handle:
        return handle.read()


# --- 2. Serialization Function ---

def serialize_animal(animal_obj):
    """
    Serializes a single animal dictionary into the required HTML card structure.
    Returns the HTML string for one <li> element.
    """
    if not isinstance(animal_obj, dict):
        return ''

    characteristics = animal_obj.get("characteristics", {})
    animal_html = ''

    # Start the HTML serialization: <li class="cards__item">
    animal_html += '<li class="cards__item">\n'

    # 1. Name: Use <div class="card__title">
    if "name" in animal_obj and isinstance(animal_obj["name"], str):
        name = animal_obj["name"].strip()
        animal_html += f'  <div class="card__title">{name}</div>\n'

    # Use a list to build the <p class="card__text"> content only if data is present
    p_content = []

    # 2. Diet
    if "diet" in characteristics and isinstance(characteristics["diet"], str):
        p_content.append(f'      <strong>Diet:</strong> {characteristics["diet"]}<br/>\n')

    # 3. First Location
    if ("locations" in animal_obj and
            isinstance(animal_obj["locations"], list) and
            animal_obj["locations"] and
            isinstance(animal_obj["locations"][0], str)):
        p_content.append(f'      <strong>Location:</strong> {animal_obj["locations"][0]}<br/>\n')

    # 4. Type
    if "type" in characteristics and isinstance(characteristics["type"], str):
        p_content.append(f'      <strong>Type:</strong> {characteristics["type"]}<br/>\n')

    # Add the <p class="card__text"> block only if characteristics were found
    if p_content:
        animal_html += '  <p class="card__text">\n'
        animal_html += "".join(p_content)
        animal_html += '  </p>\n'

    # End the HTML serialization for the current animal card
    animal_html += '</li>\n'

    return animal_html


# --- 3. Main Script Execution ---

def main():
    """Main function to orchestrate loading, serialization, replacement, and writing."""
    ANIMALS_DATA_FILE = 'animals_data.json'
    TEMPLATE_FILE = 'animals_template.html'
    OUTPUT_FILE = 'animals.html'
    PLACEHOLDER = '__REPLACE_ANIMALS_INFO__'

    # Load the data
    animals_data = load_data(ANIMALS_DATA_FILE)

    if not (animals_data and isinstance(animals_data, list)):
        print("Script terminated: Data loading failed or top-level structure is not a list.")
        return

    # Generate a single string with the animals' data serialized as the final HTML card
    animals_output_string = ''
    for animal_obj in animals_data:
        animals_output_string += serialize_animal(animal_obj)

    # Read the content of the template
    try:
        template_content = read_template(TEMPLATE_FILE)
    except Exception as e:
        print(f"ERROR: Could not read template file. Details: {e}")
        return

    # Replace the placeholder with the generated string
    final_html_content = template_content.replace(PLACEHOLDER, animals_output_string)

    # Write the new HTML content to a new file, animals.html
    try:
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write(final_html_content)
        print(f"\nSUCCESS! Content fully serialized into HTML and written to {OUTPUT_FILE}")
       # print("The code is now organized with a dedicated 'serialize_animal' function for better maintainability.")
    except Exception as e:
        print(f"\nERROR: Could not write to {OUTPUT_FILE}. Details: {e}")


if __name__ == "__main__":
    main()