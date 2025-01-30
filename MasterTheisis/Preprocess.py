
import logging
import os
import re
import shutil
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessRawData:
    # rename_file_names_in form ([technology]_[target_year(in this case 2033)]_[country_code]
    # Process raw data to obtain a table with weather year profiles for every ERAA-file
    # and format the data from availability to unavailability values (apply 1- for all values)
    def __init__(self,input_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\raw_data\\PECD",
                 output_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\processed_data"):

        self.input_path = input_path
        self.output_path = output_path
    # Function to process the 'number' DataFrame
    def format_and_transform_raw_data(self):
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.input_path, exist_ok=True)
        pattern = r"PECD_(LFSolarPV|CSP_noStorage|Wind_Offshore|Wind_Onshore)_(2033)_(\w+)_edition 2023.2"

        # Loop through each file in the input directory
        for filename in os.listdir(self.input_path):
            match = re.match(pattern, filename)
            if match:

                # Load the CSV file
                file_path = os.path.join(self.input_path, filename)
                df = pd.read_csv(file_path)

                # Split the DataFrame
                # df_stammdaten = df.head(9)
                df_number = df[10:].copy()

                # Use the row number 10 as header for the df_number
                df_number.columns = df.iloc[9]
                df_number.reset_index(drop=True, inplace=True)

                # Process the 'number' DataFrame
                df_number = self.transform_df_to_unavailability(df_number)

                # Create base names for the Excel files
                base_name = os.path.splitext(filename)[0]
                # stammdaten_name = os.path.join(output_directory, f"{base_name}_stammdaten.xlsx")
                number_name = os.path.join(self.output_path, f"{base_name}_number.xlsx")

                # Save the split DataFrames as Excel files
                # df_stammdaten.to_excel(stammdaten_name, index=False)
                df_number.to_excel(number_name, index=False)

                print(f"Processed and saved {filename} as:")
                # print(f"  {stammdaten_name}")
                # print(f"  {number_name}")
    def transform_df_to_unavailability(self,df):
        os.makedirs(self.input_path, exist_ok=True)
        # Count values that do not meet the criteria before transformations
        # non_criteria_count = df[df.columns[2:]].apply(lambda x: ((x < 0) | (x > 1)).sum()).sum()
        # nan_count = df[df.columns[2:]].isna().sum().sum()

        # print(f"Number of values not meeting the criteria: {non_criteria_count}")
        # print(f"Number of NaN values: {nan_count}")

        # Format the second column as numbers
        df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')

        # Iterate through columns starting from the third one
        for col in df.columns[2:]:
            # Find indices where values are less than 0 or greater than 1
            indices = df.index[(df[col] < 0) | (df[col] > 1)].tolist()
            for i in indices:
                # Replace value with the average of the previous and next values
                if i > 0 and i < len(df) - 1:
                    df.at[i, col] = (df.at[i - 1, col] + df.at[i + 1, col]) / 2

            # Apply the transformation value = 1 - value
            df[col] = 1 - df[col]

        # Round numbers to 4 decimal places
        df[df.columns[2:]] = df[df.columns[2:]].round(4)

        return df


class CreateShapeAFiles:
    def __init__(self,input_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\processed_data",
                 output_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\transformed_data",
                 dic_offshore_path = "C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\raw_data\\shpab_offshore.xlsx",
        dic_onshore_path = "C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\raw_data\\shpab_onshore.xlsx"):

        # create_shape_a_files

        self.input_path = input_path
        self.output_path = output_path
        self.dic_onshore_path = dic_onshore_path
        self.dic_offshore_path = dic_offshore_path

    def find_closest_key(self, lookup_value, value_map):
        """Find the closest key in the dictionary to the lookup_value."""
        keys = np.array(list(value_map.keys()))
        closest_key = keys[np.argmin(np.abs(keys - lookup_value))]
        return closest_key

    def transform(self, source):
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.input_path, exist_ok=True)
        dic_offshore = pd.read_excel(self.dic_offshore_path)
        dic_onshore = pd.read_excel(self.dic_onshore_path)
        pattern = r"PECD_(LFSolarPV|CSP_noStorage|Wind_Offshore|Wind_Onshore)_(2033)_(\w+)_edition 2023.2"
        # Loop through all files in the directory
        for filename in os.listdir(self.input_path):
            if filename.endswith("_number.xlsx") and source in filename:
                match = re.match(pattern, filename)
                if match:
                    # Load the Excel file
                    file_path = os.path.join(self.input_path, filename)
                    df = pd.read_excel(file_path)
                    old = df.copy()
                    # Read the transformation vectors
                    if source == 'Wind_Offshore':
                        trans_vecs = dic_offshore
                    elif source == 'Wind_Onshore':
                        trans_vecs = dic_onshore

                    value_map = trans_vecs.set_index(trans_vecs.columns[1])[trans_vecs.columns[0]].to_dict()

                    # Transform the values from the third column onwards
                    for column in df.columns[2:]:
                        df[column] = df[column].apply(lambda x: value_map[self.find_closest_key(x, value_map)])

                    base_name = os.path.splitext(filename)[0]
                    output_file_path = os.path.join(self.output_path, base_name + ".xlsx")

                    # Save the transformed DataFrame as an Excel file
                    df.to_excel(output_file_path, index=False)

                    print(f"Transform and saved {filename} as {output_file_path}")

    def rename_shape_a_files(self):
        input_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\transformed_data"
        output_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\processed_data3"

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
class RenameFilesNames:
    def __init__(self,input_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\processed_data",
                 output_path=r"C:\\Users\\ahmed\\Desktop\\Masterarbeit2\\Test_data\\processed_data2"):
        self.input_path = input_path
        self.output_path = output_path

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


    # use the renamed files to generate the files for special countries like balkan and baltics by weighted average
    # depending on the installed capacities for a renewable energy source
    def create_special_input_files(self):
        global columns_to_weight
        import pandas as pd
        import glob
        countries_dic = {'BT': ['LV','EE','LT'], 'BA':[], 'NO':[],'SC':[],'TR':['GR']}
        pv_dic = {'BT': [0.13,0.35,0.52], 'BA': [], 'NO': [], 'SC': [], 'TR': 1}
        wind_on_dic = {'BT': [0.07,0.24,0.69], 'BA': [], 'NO': [], 'SC': [], 'TR': 1}
        wind_off_dic = {'BT': [0,0,1], 'BA': [], 'NO': [], 'SC': [], 'TR': 1}
        # Define the countries and their weights for each technology
        country_codes = input('give the list of special countries with their country codes = ')
        for country_code in country_codes:
            special_country = input('give the list (country codes) of the countries constituting the special country as a list = ')
            weights_pv = input('give the list of the weights for pv as a list= ')
            weights_wind_on = input('give the list of the weights for wind_on as a list= ')
            weights_wind_off = input('give the list of the weights for wind_off as a list= ')

            # Define the technologies and their corresponding weights
            technologies = {
                'pv': weights_pv,
                'wind_on': weights_wind_on,
                'wind_off': weights_wind_off
            }

            # Path to the directory containing the files (adjust as needed)
            os.makedirs(self.output_path, exist_ok=True)
            file_path = self.output_path  # replace with your directory path (output and input path are the same)

            # Iterate through each technology
            for tech, weights in technologies.items():
                data_list = []

                # Iterate through each country for the specific technology
                for country, weight in zip(special_country, weights):
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
                    output_file = f"{file_path}/{tech}_2033_{country_code}.xlsx"
                    combined_data.to_excel(output_file, index=False)
                    print(f"Created file: {output_file}")


class PrepareDataBaseFiles:

    def __init__(self, input_path, output_path, weather_years):
        self.input_path = input_path
        self.weather_years = weather_years
        self.output_path = output_path
    def prepare_data_base_files_1(self):
        data_dict = {
            4832: "pv_2033_DE00",
            4866: "pv_2033_BT",
            4851: "pv_2033_TR00",
            4857: "pv_2033_BA",
            4823: "pv_2033_FR00",
            4802: "pv_2033_BE00",
            4819: "pv_2033_AT00",
            4806: "pv_2033_CH00",
            4855: "pv_2033_NL00",
            4878: "pv_2033_PL00",
            4817: "pv_2033_CZ00",
            4824: "pv_2033_DKW1",
            4827: "pv_2033_DKE1",
            4848: "pv_2033_SC",
            4845: "pv_2033_SE01",
            3678: "pv_2033_ITCN",
            4861: "pv_2033_UK00",
            4865: "pv_2033_ITN1",
            4805: "csp_2033_ES00",
            4803: "pv_2033_ES00",
            4809: "pv_2033_RO00",
            4833: "pv_2033_SK00",
            4872: "pv_2033_HU00",
            4797: "pv_2033_BG00",
            4838: "pv_2033_GR00",
            4812: "pv_2033_PT00",
            4869: "pv_2033_NO",
            4875: "pv_2033_FI00",
            3295: "pv_2033_ITCS",
            4839: "pv_2033_SE03",
            4843: "pv_2033_SE04",
            3675: "pv_2033_ITS1",
            4863: "pv_2033_ITSI",
            2923: "pv_2033_ITSA",
            663: "pv_2033_ITCA",
            4748: "wind_on_2033_DE00_shape_a",
            4782: "wind_on_2033_BT_shape_a",
            4767: "wind_on_2033_TR00_shape_a",
            4773: "wind_on_2033_BA_shape_a",
            4739: "wind_on_2033_FR00_shape_a",
            4716: "wind_on_2033_BE00_shape_a",
            4734: "wind_on_2033_AT00_shape_a",
            4722: "wind_on_2033_CH00_shape_a",
            4770: "wind_on_2033_NL00_shape_a",
            4796: "wind_on_2033_PL00_shape_a",
            4731: "wind_on_2033_CZ00_shape_a",
            4740: "wind_on_2033_DKW1_shape_a",
            4743: "wind_on_2033_DKE1_shape_a",
            4764: "wind_on_2033_SC_shape_a",
            4761: "wind_on_2033_SE01_shape_a",
            4715: "wind_on_2033_ITCN_shape_a",
            4776: "wind_on_2033_UK00_shape_a",
            4781: "wind_on_2033_ITN1_shape_a",
            4721: "wind_on_2033_ES00_shape_a",
            4725: "wind_on_2033_RO00_shape_a",
            4749: "wind_on_2033_SK00_shape_a",
            4788: "wind_on_2033_HU00_shape_a",
            4713: "wind_on_2033_BG00_shape_a",
            4752: "wind_on_2033_GR00_shape_a",
            4730: "wind_on_2033_PT00_shape_a",
            4785: "wind_on_2033_NO_shape_a",
            4791: "wind_on_2033_FI00_shape_a",
            4719: "wind_on_2033_ITCS_shape_a",
            4755: "wind_on_2033_SE03_shape_a",
            4758: "wind_on_2033_SE04_shape_a",
            4723: "wind_on_2033_ITSI_shape_a",
            4726: "wind_on_2033_ITS1_shape_a",
            4728: "wind_on_2033_ITSA_shape_a",
            679: "wind_on_2033_ITCA_shape_a",
            4718: "wind_on_2033_ITCN",
            4714: "wind_on_2033_ITN1",
            4720: "wind_on_2033_ITCS",
            4724: "wind_on_2033_ITS1",
            4727: "wind_on_2033_ITSI",
            4729: "wind_on_2033_ITSA",
            1289: "wind_on_2033_ITCA",
            4732: "wind_on_2033_DE00",
            4733: "wind_on_2033_BT",
            4735: "wind_on_2033_TR00",
            4736: "wind_on_2033_BA",
            4737: "wind_on_2033_FR00",
            4742: "wind_on_2033_BE00",
            4745: "wind_on_2033_AT00",
            4747: "wind_on_2033_CH00",
            4750: "wind_on_2033_NL00",
            4751: "wind_on_2033_PL00",
            4753: "wind_on_2033_CZ00",
            4754: "wind_on_2033_DKW1",
            4756: "wind_on_2033_DKE1",
            4760: "wind_on_2033_SC",
            4762: "wind_on_2033_SE01",
            4763: "wind_on_2033_UK00",
            4765: "wind_on_2033_ES00",
            4766: "wind_on_2033_RO00",
            4768: "wind_on_2033_SK00",
            4769: "wind_on_2033_HU00",
            4772: "wind_on_2033_BG00",
            4774: "wind_on_2033_GR00",
            4775: "wind_on_2033_PT00",
            4778: "wind_on_2033_NO",
            4779: "wind_on_2033_FI00",
            4780: "wind_on_2033_SE03",
            4783: "wind_on_2033_SE04",
            4746: "wind_off_2033_DE00_shape_a",
            4738: "wind_off_2033_FR00_shape_a",
            4717: "wind_off_2033_BE00_shape_a",
            4771: "wind_off_2033_NL00_shape_a",
            4741: "wind_off_2033_DKW1_shape_a",
            4744: "wind_off_2033_DKE1_shape_a",
            4777: "wind_off_2033_UK00_shape_a",
            4759: "wind_off_2033_SE04_shape_a",
            4757: "wind_off_2033_SE03_shape_a",
            4794: "wind_off_2033_PL00_shape_a",
            4784: "wind_off_2033_DE00",
            4786: "wind_off_2033_UK00",
            64: "wind_off_2033_FI00_shape_a",
            275: "wind_off_2033_BT_shape_a",
            1639: "wind_off_2033_NO_shape_a",
            955: "wind_off_2033_ES00_shape_a"

        }
        number_of_added_files = 0

        os.makedirs(self.output_path, exist_ok=True)
        logging.info(f"Output directory set to: {self.output_path}")
        for year in self.weather_years:
            # Initialize an empty DataFrame with required columns
            pp_non_ava = pd.DataFrame(columns=['VARID', 'KWID', 'PKTNR', 'REVNV', 'RID'])
            logging.info(f"Processing weather year: {year}")

            # Loop through each key in the dictionary
            for pp_id, file_prefix in data_dict.items():
                # Find files that start with the specified prefix
                found_files = [f for f in os.listdir(self.input_path) if f == (file_prefix + '.xlsx')]

                if found_files:
                    # Process each file that matches the prefix
                    for file_name in found_files:
                        file_path = os.path.join(self.input_path, file_name)
                        logging.info(f"Found file for PP_ID {pp_id}: {file_path}")

                        # Read the Excel file
                        df = pd.read_excel(file_path)

                        # Ensure the file has the required columns (Hour and the specific year)
                        if year in df.columns:
                            # Create a temporary DataFrame for this key
                            temp_df = pd.DataFrame({
                                'VARID': [1003] * len(df),
                                'KWID': [pp_id] * len(df),
                                'PKTNR': df.index + 1,  # 'Hour' column as 'LP_NR'
                                'REVNV': round(df[year], 4),  # Specific year column as 'REV_NONAVAIL'
                                'RID': [''] * len(df)  # RID is empty
                            })

                            # Concatenate the temp DataFrame to the main DataFrame for this year
                            pp_non_ava = pd.concat([pp_non_ava, temp_df], ignore_index=True)
                            logging.info(f"Data from {file_name} for year {year} added to the DataFrame.")
                            number_of_added_files = number_of_added_files + 1
                        else:
                            logging.warning(f"File {file_path} missing required columns for year {year}. Skipping.")
                else:
                    logging.warning(f"No files found starting with {file_prefix} for PP_ID {pp_id}")

            # Save the DataFrame to an Excel file for this specific weather year
            output_file_path = os.path.join(self.output_path, f"{year}")
            os.makedirs(output_file_path, exist_ok=True)
            output_file_path = os.path.join(output_file_path, f"WeatherYear_{year}_1.csv")
            pp_non_ava.to_csv(output_file_path, index=False)
            logging.info(f"Created file: {output_file_path}")
            logging.info(f"Created file: {output_file_path}")
            print('number_of_added_files = ', number_of_added_files, '   Soll = 119')

    def prepare_data_base_files_2(self):
        data_dict = {

            1830: "wind_off_2033_PT00_shape_a",
            1646: "wind_off_2033_ITSA_shape_a",
            1642: "wind_off_2033_ITSI_shape_a"
        }

        number_of_added_files = 0

        for year in self.weather_years:
            # Initialize an empty DataFrame with required columns
            pp_non_ava = pd.DataFrame(columns=['VARID', 'KWID', 'PKTNR', 'REVNV', 'RID'])
            logging.info(f"Processing weather year: {year}")

            # Loop through each key in the dictionary
            for pp_id, file_prefix in data_dict.items():
                # Find files that start with the specified prefix
                found_files = [f for f in os.listdir(self.input_path) if f == (file_prefix + '.xlsx')]

                if found_files:
                    # Process each file that matches the prefix
                    for file_name in found_files:
                        file_path = os.path.join(self.input_path, file_name)
                        logging.info(f"Found file for PP_ID {pp_id}: {file_path}")

                        # Read the Excel file
                        df = pd.read_excel(file_path)

                        # Ensure the file has the required columns (Hour and the specific year)
                        if year in df.columns:
                            # Create a temporary DataFrame for this key
                            temp_df = pd.DataFrame({
                                'VARID': [1003] * len(df),
                                'KWID': [pp_id] * len(df),
                                'PKTNR': df.index + 1,  # 'Hour' column as 'LP_NR'
                                'REVNV': round(df[year], 4),  # Specific year column as 'REV_NONAVAIL'
                                'RID': [''] * len(df)  # RID is empty
                            })

                            # Concatenate the temp DataFrame to the main DataFrame for this year
                            pp_non_ava = pd.concat([pp_non_ava, temp_df], ignore_index=True)
                            logging.info(f"Data from {file_name} for year {year} added to the DataFrame.")
                            number_of_added_files = number_of_added_files + 1
                        else:
                            logging.warning(f"File {file_path} missing required columns for year {year}. Skipping.")
                else:
                    logging.warning(f"No files found starting with {file_prefix} for PP_ID {pp_id}")

            # Save the DataFrame to an Excel file for this specific weather year
            output_file_path = os.path.join(self.output_path, f"{year}")
            os.makedirs(output_file_path, exist_ok=True)
            output_file_path = os.path.join(output_file_path, f"WeatherYear_{year}_2.csv")
            pp_non_ava.to_csv(output_file_path, index=False)
            logging.info(f"Created file: {output_file_path}")
            print('number_of_added_files = ', number_of_added_files, '   Soll = 3')
