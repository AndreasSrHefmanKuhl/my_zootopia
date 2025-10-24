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

    # 2. Generate single string with the animals' data serialized as HTML
    animals_output_string = ''

    # Iterate through the animals
    for animal in animals_data:
        if not isinstance(animal, dict):
            continue

        # List to store the field printouts for this animal, including the <br/> and \n
        output_parts = []
        characteristics = animal.get("characteristics", {})

        # Start the HTML serialization for the current animal card
        output_parts.append('<li class="cards__item">\n')

        #  Name (Key: "name")
        if "name" in animal and isinstance(animal["name"], str):
            # Append with <br/>\n as required
            output_parts.append(f"Name: {animal['name']}<br/>\n")

        # Diet (Key: "characteristics" -> "diet")
        if "diet" in characteristics and isinstance(characteristics["diet"], str):
            output_parts.append(f"Diet: {characteristics['diet']}<br/>\n")

        #  First Location (Key: "locations")
        if ("locations" in animal and
                isinstance(animal["locations"], list) and
                animal["locations"] and
                isinstance(animal["locations"][0], str)):
            output_parts.append(f"Location: {animal['locations'][0]}<br/>\n")

        #  Type (Key: "characteristics" -> "type")
        if "type" in characteristics and isinstance(characteristics["type"], str):
            output_parts.append(f"Type: {characteristics['type']}<br/>\n")

        # End the HTML serialization for the current animal card
        # Note: The original example showed the closing </li> immediately following the last <br/>
        output_parts.append('</li>\n')

        # Append the completed HTML block for this animal to the total string
        animals_output_string += "".join(output_parts)

    #  Read the content of the template
    template_content = read_template(TEMPLATE_FILE)

    #  Replace __REPLACE_ANIMALS_INFO__ with the generated string
    final_html_content = template_content.replace(PLACEHOLDER, animals_output_string)

    #  Write the new HTML content to a new file, animals.html
    try:
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write(final_html_content)
        print(f"\nSUCCESS: Content serialized to HTML and written to {OUTPUT_FILE}")
        #print("Commit your changes with a message akin to 'generate card item for every animal'.")
    except Exception as e:
        print(f"\nERROR: Could not write to {OUTPUT_FILE}. Details: {e}")

else:
    print("Script terminated due to error in loading data.")