import json
import os


# --- 1. Robust Data Loading Function ---
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


# --- 2. Template Reading Function ---
def read_template(file_path):
    """ Reads the content of an HTML template file. """
    with open(file_path, "r", encoding='utf-8') as handle:
        return handle.read()


# --- 3. Main Logic ---

ANIMALS_DATA_FILE = 'animals_data.json'
TEMPLATE_FILE = 'animals_template.html'
OUTPUT_FILE = 'animals.html'
PLACEHOLDER = '__REPLACE_ANIMALS_INFO__'

# Load the data
animals_data = load_data(ANIMALS_DATA_FILE)

if animals_data and isinstance(animals_data, list):

    # 2. Generate a single string with the animals' data serialized as the final HTML card
    animals_output_string = ''

    # Iterate through the animals
    for animal in animals_data:
        if not isinstance(animal, dict):
            continue

        characteristics = animal.get("characteristics", {})

        # Start the HTML serialization for the current animal card
        animal_html = '<li class="cards__item">\n'

        # 1. Name: Use <div class="card__title">
        if "name" in animal and isinstance(animal["name"], str):
            # Trim for cleaner look, but ensure the data is safe
            name = animal["name"].strip()
            animal_html += f'  <div class="card__title">{name}</div>\n'

        # Start the characteristics block: <p class="card__text">
        # Use a temporary list to build the <p> content only if data is present
        p_content = []

        # 2. Diet
        if "diet" in characteristics and isinstance(characteristics["diet"], str):
            p_content.append(f'      <strong>Diet:</strong> {characteristics["diet"]}<br/>\n')

        # 3. First Location
        if ("locations" in animal and
                isinstance(animal["locations"], list) and
                animal["locations"] and
                isinstance(animal["locations"][0], str)):
            p_content.append(f'      <strong>Location:</strong> {animal["locations"][0]}<br/>\n')

        # 4. Type
        if "type" in characteristics and isinstance(characteristics["type"], str):
            p_content.append(f'      <strong>Type:</strong> {characteristics["type"]}<br/>\n')

        # Only add the <p class="card__text"> block if there is content for it
        if p_content:
            animal_html += '  <p class="card__text">\n'
            animal_html += "".join(p_content)
            animal_html += '  </p>\n'

        # End the HTML serialization for the current animal card
        animal_html += '</li>\n'

        # Append the completed HTML block for this animal to the total string
        animals_output_string += animal_html

    # 1. Read the content of the template
    template_content = read_template(TEMPLATE_FILE)

    # 3. Replace __REPLACE_ANIMALS_INFO__ with the generated string
    final_html_content = template_content.replace(PLACEHOLDER, animals_output_string)

    # 4. Write the new HTML content to a new file, animals.html
    try:
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write(final_html_content)
        print(f"\nSUCCESS! Content fully serialized into HTML and written to {OUTPUT_FILE}")
        print("You can now open 'animals.html' in your browser to view the final result.")

    except Exception as e:
        print(f"\nERROR: Could not write to {OUTPUT_FILE}. Details: {e}")

else:
    print("Script terminated due to error in loading data.")