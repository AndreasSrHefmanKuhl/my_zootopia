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
        # Handle malformed JSON data
        print(f"ERROR: Failed to decode JSON from {file_path}. Details: {e}")
        return None
    except Exception as e:

        print(f"ERROR: An unexpected error occurred while reading {file_path}. Details: {e}")
        return None


# --- 2. Main Logic ---

FILE_PATH = 'animals_data.json'

# Load the data
animals_data = load_data(FILE_PATH)

# Check if the loading was successful AND the data is the expected type (a list)
if animals_data and isinstance(animals_data, list):

    # Iterate through the animals
    for i, animal in enumerate(animals_data):

        if not isinstance(animal, dict):
            print(f"WARNING: Skipping item at index {i} as it is not a dictionary.")
            continue

        # List to store the field printouts for this animal
        output_parts = []

        #  .get() to safely access 'characteristics', defaulting to an empty dict {}
        characteristics = animal.get("characteristics", {})


        # Added check for expected type (str)
        if "name" in animal and isinstance(animal["name"], str):
            output_parts.append(f"Name: {animal['name']}")

        #  Diet (Key: "characteristics" -> "diet")
        if "diet" in characteristics and isinstance(characteristics["diet"], str):
            output_parts.append(f"Diet: {characteristics['diet']}")

        # First Location (Key: "locations")
        # Check if 'locations' key exists, is a list, AND is not empty
        if ("locations" in animal and
                isinstance(animal["locations"], list) and
                animal["locations"] and
                isinstance(animal["locations"][0], str)):  # Also check the type of the item itself

            output_parts.append(f"Location: {animal['locations'][0]}")

        #  Type (Key: "characteristics" -> "type")
        if "type" in characteristics and isinstance(characteristics["type"], str):
            output_parts.append(f"Type: {characteristics['type']}")

        # Print the data if successfully extracted any fields
        if output_parts:
            # Print each part on a new line
            for part in output_parts:
                print(part)

            # Print an extra blank line to separate animal entries
            print()

else:
    # block executes if the file failed to load, or the top-level data structure
    if animals_data is not None:
        print(f"ERROR: Expected top-level JSON to be a list, but got {type(animals_data)}.")
    print("Script terminated without printing data due to file or data structure errors.")