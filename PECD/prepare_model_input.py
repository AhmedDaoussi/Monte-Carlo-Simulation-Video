import logging
import os
import re
import shutil

import pandas as pd

data_dict = {
    4832: "pv_2033_DE",
    4802: "pv_2033_BE",
    4819: "pv_2033_AT",
    4806: "pv_2033_CH",
    4855: "pv_2033_NL",
    4878: "pv_2033_DK2",
    4817: "pv_2033_CZ",
    4824: "pv_2033_DKW1",
    4827: "pv_2033_DKE1",
    3678: "pv_2033_ITCN",
    4861: "pv_2033_GB",
    4865: "pv_2033_ITN1",
    4805: "csp_2033_ES",
    4803: "pv_2033_ES",
    4809: "pv_2033_RO",
    4833: "pv_2033_SK",
    4872: "pv_2033_BG",
    4797: "pv_2033_BG",
    4838: "pv_2033_GR",
    4812: "pv_2033_PT",
    4875: "pv_2033_FI",
    3295: "pv_2033_ITCS",
    4839: "pv_2033_SE03",
    4843: "pv_2033_SE04",
    3675: "pv_2033_ITS1",
    4863: "pv_2033_ITSI",
    2923: "pv_2033_ITSA",
    663: "pv_2033_ITCA",
    4718: "wind_on_2033_ITCN",
    4714: "wind_on_2033_ITN1",
    4720: "wind_on_2033_ITCS",
    4724: "wind_on_2033_ITS1",
    4727: "wind_on_2033_ITSI",
    4729: "wind_on_2033_ITSA",
    1289: "wind_on_2033_ITCA",
    4732: "wind_on_2033_DE",
    4737: "wind_on_2033_FR",
    4742: "wind_on_2033_BE",
    4745: "wind_on_2033_AT",
    4747: "wind_on_2033_CH",
    4750: "wind_on_2033_NL",
    4751: "wind_on_2033_DK2",
    4753: "wind_on_2033_CZ",
    4754: "wind_on_2033_DKW1",
    4756: "wind_on_2033_DKE1",
    4763: "wind_on_2033_GB",
    4765: "wind_on_2033_ES",
    4766: "wind_on_2033_RO",
    4768: "wind_on_2033_SK",
    4769: "wind_on_2033_BG",
    4772: "wind_on_2033_BG",
    4774: "wind_on_2033_GR",
    4775: "wind_on_2033_PT",
    4779: "wind_on_2033_FI",
    4780: "wind_on_2033_SE03",
    4783: "wind_on_2033_SE04",
    4746: "wind_off_2033_DE",
    4738: "wind_off_2033_FR",
    4717: "wind_off_2033_BE",
    4771: "wind_off_2033_NL",
    4741: "wind_off_2033_DKW1",
    4744: "wind_off_2033_DKE1",
    4777: "wind_off_2033_GB",
    4759: "wind_off_2033_SE04",
    4757: "wind_off_2033_SE03",
    4794: "wind_off_2033_PL",
    64: "wind_off_2033_FI",
    955: "wind_off_2033_ES",
    1830: "wind_off_2033_PT",
    1646: "wind_off_2033_ITSA",
    1642: "wind_off_2033_ITSI",
    4851: "pv_2033_TR",
    4735: "wind_on_2033_TR"
}
class PrepareModelInput:
    def __init__(self):
        self.input_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data"
        self.output_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data2"
        self.output_path_weather_years = r'C:\Users\ahmed\Desktop\Masterarbeit\Weather_Year_Files'

    def rename_file_names(self):
        # Ensure the output directory exists
        os.makedirs(self.output_path, exist_ok=True)

        # Regular expression pattern to match files
        pattern = r"PECD_(LFSolarPV|CSP_noStorage|Wind_Offshore|Wind_Onshore)_(\d{4})_(\w+)_edition 2023\.2_number"

        # Loop through each file in the input directory
        for filename in os.listdir(self.input_path):
            match = re.match(pattern, filename)
            if match:
                type_part, ty, cc = match.groups()

                # Only process files with ty equal to 2033
                if ty == "2033":
                    if type_part == "LFSolarPV":
                        new_filename = f"pv_{ty}_{cc}.xlsx"
                    elif type_part == "CSP_noStorage":
                        new_filename = f"csp__{ty}_{cc}.xlsx"
                    elif type_part == "Wind_Offshore":
                        new_filename = f"wind_off_{ty}_{cc}.xlsx"
                    elif type_part == "Wind_Onshore":
                        new_filename = f"wind_on_{ty}_{cc}.xlsx"
                    else:
                        continue

                    # Copy the file to the output directory with the new name
                    src = os.path.join(self.input_path, filename)
                    dst = os.path.join(self.output_path, new_filename)
                    shutil.copy(src, dst)
                    print(f"Renamed '{filename}' to '{new_filename}'")

    def create_input_files(self):
        # Ensure output directory exists
        os.makedirs(self.output_path_weather_years, exist_ok=True)
        logging.info(f"Output directory set to: {self.output_path_weather_years}")

        # Weather years to iterate over
        weather_years = list(range(1982, 1983))  # From 1982 to 2019

        # Loop through each weather year
        for year in weather_years:
            # Initialize an empty DataFrame with required columns
            pp_non_ava = pd.DataFrame(columns=['VARID', 'PP_ID', 'LP_NR', 'REV_NONAVAIL', 'RID'])
            logging.info(f"Processing weather year: {year}")

            # Loop through each key in the dictionary
            for pp_id, file_prefix in data_dict.items():
                # Find files that start with the specified prefix
                found_files = [f for f in os.listdir(self.output_path) if f.startswith(file_prefix)]

                if found_files:
                    # Process each file that matches the prefix
                    for file_name in found_files:
                        file_path = os.path.join(self.output_path, file_name)
                        logging.info(f"Found file for PP_ID {pp_id}: {file_path}")

                        # Read the Excel file
                        df = pd.read_excel(file_path)

                        # Ensure the file has the required columns (Hour and the specific year)
                        if year in df.columns:
                            # Create a temporary DataFrame for this key
                            temp_df = pd.DataFrame({
                                'VARID': [1003] * len(df),
                                'PP_ID': [pp_id] * len(df),
                                'LP_NR': df.index - 1,  # 'Hour' column as 'LP_NR'
                                'REV_NONAVAIL': df[year],  # Specific year column as 'REV_NONAVAIL'
                                'RID': [''] * len(df)  # RID is empty
                            })

                            # Concatenate the temp DataFrame to the main DataFrame for this year
                            pp_non_ava = pd.concat([pp_non_ava, temp_df], ignore_index=True)
                            logging.info(f"Data from {file_name} for year {year} added to the DataFrame.")
                        else:
                            logging.warning(f"File {file_path} missing required columns for year {year}. Skipping.")
                else:
                    logging.warning(f"No files found starting with {file_prefix} for PP_ID {pp_id}")

            # Save the DataFrame to an Excel file for this specific weather year
            output_file_path = os.path.join(self.output_path_weather_years, f"WeatherYear_{year}.xlsx")
            pp_non_ava.to_excel(output_file_path, index=False)
            logging.info(f"Created file: {output_file_path}")

    def create_special_input_files(self):
        global columns_to_weight
        import pandas as pd
        import glob

        # Define the countries and their weights for each technology
        baltic_countries = ['LT', 'LV', 'EE']
        weights_pv = [0.513, 0.133, 0.353]
        weights_wind = [0.69, 0.07, 0.24]

        # Define the technologies and their corresponding weights
        technologies = {
            'pv': weights_pv,
            'wind_on': weights_wind,
            'wind_off': weights_wind
        }

        # Path to the directory containing the files (adjust as needed)
        file_path = self.output_path  # replace with your directory path

        # Iterate through each technology
        for tech, weights in technologies.items():
            data_list = []

            # Iterate through each country for the specific technology
            for country, weight in zip(baltic_countries, weights):
                # Construct the filename pattern to load
                file_pattern = f"{file_path}/{tech}_2033_{country}00.xlsx"

                # Load the Excel file if it exists
                try:
                    df = pd.read_excel(file_pattern)

                    # Apply the weight only to columns from '1982' to '2019'
                    columns_to_weight = [col for col in df.columns[2:]]
                    df_weighted = df.copy()
                    df_weighted[columns_to_weight] = df[
                                                         columns_to_weight] * weight  # Apply weight only to specified columns
                    data_list.append(df_weighted)

                except FileNotFoundError:
                    print(f"File not found: {file_pattern}")
                    continue

            # Combine all weighted data for this technology
            if data_list:
                combined_data = pd.concat(data_list)

                # Group by 'date' and 'hour' columns and sum the weighted columns
                combined_data = combined_data.groupby(['Date', 'Hour'])[columns_to_weight].sum().reset_index()

                # Save the result to a new Excel file
                output_file = f"{file_path}/{tech}_2033_BT.xlsx"
                combined_data.to_excel(output_file, index=False)
                print(f"Created file: {output_file}")
