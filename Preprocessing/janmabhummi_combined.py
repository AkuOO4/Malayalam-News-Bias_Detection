import os
import json
import random
import re
# Path to the folder containing .utf8 files
folder_path = "Data\Janmabhumi" # <-- change this

# Get all .utf8 files
all_files = [f for f in os.listdir(folder_path) if f.endswith('.utf8')]

# Pick 100 random files
selected_files = random.sample(all_files, 100)

# Create a list to hold data
data = []

def remove_english_letters(text):
    # This regex matches any English letter (both lowercase and uppercase)
    cleaned_text = re.sub(r'[a-zA-Z]', '', text)
    return cleaned_text

# Read and store content
for filename in selected_files:
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = remove_english_letters(content)
    data.append({
        'content': content,
        'label': 'right'
    })

# Save to a single JSON file
output_path = 'Data/news/Janmabhumi.json'  # <-- output file
with open(output_path, 'w', encoding='utf-8') as out_file:
    json.dump(data, out_file, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} files into {output_path}")
