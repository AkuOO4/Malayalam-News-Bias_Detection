import os
import json
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm  # progress bar

# Settings
input_folder = "./Data/news"  # replace with your folder path
output_folder = "./Data/Final_data"  # where you want to save train/val files
train_ratio = 0.8  # 80% train, 20% validation
random_seed = 42  # for reproducibility

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Step 1: Read, combine and process all JSON files
all_data = []

# List all JSON files first
json_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

# Loop through files with tqdm progress bar
for filename in tqdm(json_files, desc="Processing JSON files"):
    filepath = os.path.join(input_folder, filename)
    try:

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Iterate through each URL-based entry
            for url, entry in data.items():
                title = entry.get('title', '')
                content = entry.get('content', '')
                label = entry.get('label')

                # Only accept entries where content exists
                if content and label is not None:
                    combined_text = f"{title.strip()} {content.strip()}".strip()
                    all_data.append({
                        "text": combined_text,
                        "label": label
                    })
                elif title and content == "":  # Accept if only title is there and no content
                    combined_text = title.strip()
                    all_data.append({
                        "text": combined_text,
                        "label": label
                    })

    except Exception as e:
            print(f"Error processing entry for URL {url}: {e}")
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    entries = data
                else:
                    entries = [data]
                
                for entry in entries:
                    title = entry.get('title', '')
                    content = entry.get('content', '')
                    label = entry.get('label')

                    # Only accept if content exists
                    if content and label is not None:
                        combined_text = f"{title.strip()} {content.strip()}".strip()
                        all_data.append({
                            "text": combined_text,
                            "label": label
                        })
                
            

    print(f"\nTotal processed records: {len(all_data)}")

# Step 2: Shuffle the data
random.seed(random_seed)
random.shuffle(all_data)

# Step 3: Split into train and validation
train_data, val_data = train_test_split(
    all_data, train_size=train_ratio, random_state=random_seed
)

print(f"Train size: {len(train_data)}, Validation size: {len(val_data)}")

# Step 4: Save JSON files
with open(os.path.join(output_folder, "train.json"), "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

with open(os.path.join(output_folder, "val.json"), "w", encoding="utf-8") as f:
    json.dump(val_data, f, indent=2, ensure_ascii=False)

# Step 5: Save CSV files
train_df = pd.DataFrame(train_data)
val_df = pd.DataFrame(val_data)

train_df.to_csv(os.path.join(output_folder, "train.csv"), index=False)
val_df.to_csv(os.path.join(output_folder, "val.csv"), index=False)

print("✅ Data successfully processed and saved!")
