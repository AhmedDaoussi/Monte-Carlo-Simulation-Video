import os
import re
import shutil

# Define input and output paths
input_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\transformed_data"
output_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data3"

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Regular expression pattern to match files
pattern = r"PECD_(LFSolarPV|CSP_noStorage|Wind_Offshore|Wind_Onshore)_(\d{4})_(\w+)_edition 2023\.2_number"

# Loop through each file in the input directory
for filename in os.listdir(input_path):
    match = re.match(pattern, filename)
    if match:
        type_part, ty, cc = match.groups()

        # Only process files with ty equal to 2033
        if ty == "2033":

            if type_part == "Wind_Offshore":
                new_filename = f"wind_off_{ty}_{cc}_shape_a.xlsx"
            elif type_part == "Wind_Onshore":
                new_filename = f"wind_on_{ty}_{cc}_shape_a.xlsx"
            else:
                continue

            # Copy the file to the output directory with the new name
            src = os.path.join(input_path, filename)
            dst = os.path.join(output_path, new_filename)
            shutil.copy(src, dst)
            print(f"Renamed '{filename}' to '{new_filename}'")
