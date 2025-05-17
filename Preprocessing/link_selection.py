import os

# List of file pairs
file_pairs = [
    ('Data/asianet_news.txt', 'Data/asianet_news_categories.txt'),
    ('Data\deshabhimani.txt', 'Data\deshabhimani_categories.txt'),
    ('Data\mathrubhumi.txt', 'Data\mathrubhumi_categories.txt'),
    ('Data/reporter.txt','Data/reporter_categories.txt'),
    ('Data/true_Copy.txt','Data/true_Copy_categories.txt'),
    ('Data\manorama_news.txt','Data\manorama_news_categories.txt')
    # Add more pairs here
]

# Output folder
output_folder = 'Data/accepted_links'
os.makedirs(output_folder, exist_ok=True)

# Process each pair
for idx, (file_a, file_b) in enumerate(file_pairs, start=1):
    print(f"\nProcessing Pair {idx}: {file_a} & {file_b}")
    
    # Read links from A
    with open(file_a, 'r') as fa:
        links_a = [line.strip() for line in fa if line.strip()]
    
    # Read prefixes from B
    with open(file_b, 'r') as fb:
        prefixes_b = [line.strip() for line in fb if line.strip()]
    
    # Filter accepted links
    accepted_links = []
    for link in links_a:
        if any(link.startswith(prefix) for prefix in prefixes_b):
            accepted_links.append(link)
    
    # Ensure uniqueness
    unique_links = set(accepted_links)
    
    # Save to output file
    output_file = os.path.join(output_folder, f"accepted_{idx}.txt")
    with open(output_file, 'w') as fout:
        for link in unique_links:
            fout.write(link + '\n')
    
    # Report
    print(f"  Total Accepted Links: {len(accepted_links)}")
    print(f"  Unique Accepted Links: {len(unique_links)}")

    
    print(f"  Saved to {output_file}")

print("\nDone processing all file pairs.")
