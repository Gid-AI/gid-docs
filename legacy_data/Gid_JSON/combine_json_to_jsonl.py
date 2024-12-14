import json

# Define paths for input and output files
input_file_path = r"C:\Users\vervi\OneDrive\Bureau\Gid_AI\Gid_JSON\GID_75traits.json"
output_file_path = r"C:\Users\vervi\OneDrive\Bureau\Gid_AI\Gid_JSON\GID_75traits.jsonl"

# Open the input JSON file and load the content
with open(input_file_path, 'r') as json_file:
    data = json.load(json_file)

# Open the output file in write mode
with open(output_file_path, 'w') as jsonl_file:
    # Check if the top-level data has a "traits" key for categories
    if "traits" in data:
        categories = data["traits"]
        
        # Loop through each category
        for category in categories:
            # Check if each category has a "traits" list
            if "traits" in category:
                for trait in category["traits"]:
                    # Add the category information to each trait for context
                    trait["category"] = category.get("category", "Unknown")
                    # Write each trait as a separate line in JSONL format
                    jsonl_file.write(json.dumps(trait) + '\n')

print("Conversion completed successfully! Each trait is now on a separate line in JSONL.")
