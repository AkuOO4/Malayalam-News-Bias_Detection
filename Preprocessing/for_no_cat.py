# Input and output filenames
input_file = 'Data\jaihind.txt'
output_file = 'Data/accepted_links/jaihind_accepted.txt'

# Read all lines from the input file
with open(input_file, 'r') as fin:
    lines = [line.strip() for line in fin if line.strip()]

# Keep only unique lines
unique_lines = set(lines)

# Save unique lines to output file
with open(output_file, 'w') as fout:
    for line in unique_lines:
        fout.write(line + '\n')

print(f"✅ Unique {len(unique_lines)} lines saved to '{output_file}'.")
