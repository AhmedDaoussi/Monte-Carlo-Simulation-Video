import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Dictionary mapping PP_ID to file names (example data structure)
data_dict = {


    1830: "wind_off_2033_PT00_shape_a",
    1646: "wind_off_2033_ITSA_shape_a",
    1642: "wind_off_2033_ITSI_shape_a"
}


number_of_added_files= 0

# Path to the processed data folder
input_path = r'C:\Users\ahmed\Desktop\Masterarbeit\Test_data\processed_data2'
output_path = r'C:\Users\ahmed\Desktop\Masterarbeit\Weather_Year_Files'

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)
logging.info(f"Output directory set to: {output_path}")

# Weather years to iterate over
weather_years = list(range(1986, 2020))  # From 1982 to 2019

# Loop through each weather year
for year in weather_years:
    # Initialize an empty DataFrame with required columns
    pp_non_ava = pd.DataFrame(columns=['VARID', 'KWID','PKTNR', 'REVNV', 'RID'])
    logging.info(f"Processing weather year: {year}")

    # Loop through each key in the dictionary
    for pp_id, file_prefix in data_dict.items():
        # Find files that start with the specified prefix
        found_files =  [f for f in os.listdir(input_path) if f == (file_prefix+'.xlsx')]

        if found_files:
            # Process each file that matches the prefix
            for file_name in found_files:
                file_path = os.path.join(input_path, file_name)
                logging.info(f"Found file for PP_ID {pp_id}: {file_path}")

                # Read the Excel file
                df = pd.read_excel(file_path)

                # Ensure the file has the required columns (Hour and the specific year)
                if year in df.columns:
                    # Create a temporary DataFrame for this key
                    temp_df = pd.DataFrame({
                        'VARID': [1003] * len(df),
                        'KWID': [pp_id] * len(df),
                        'PKTNR': df.index +1,               # 'Hour' column as 'LP_NR'
                        'REVNV': round(df[year],4),     # Specific year column as 'REV_NONAVAIL'
                        'RID': [''] * len(df)                # RID is empty
                    })

                    # Concatenate the temp DataFrame to the main DataFrame for this year
                    pp_non_ava = pd.concat([pp_non_ava, temp_df], ignore_index=True)
                    logging.info(f"Data from {file_name} for year {year} added to the DataFrame.")
                    number_of_added_files = number_of_added_files+1
                else:
                    logging.warning(f"File {file_path} missing required columns for year {year}. Skipping.")
        else:
            logging.warning(f"No files found starting with {file_prefix} for PP_ID {pp_id}")

    # Save the DataFrame to an Excel file for this specific weather year
    output_file_path = os.path.join(output_path, f"{year}")
    os.makedirs(output_file_path, exist_ok=True)
    output_file_path = os.path.join(output_file_path, f"WeatherYear_{year}_beta.csv")
    pp_non_ava.to_csv(output_file_path, index=False)
    logging.info(f"Created file: {output_file_path}")
    print('number_of_added_files = ', number_of_added_files, '   Soll = 3')
