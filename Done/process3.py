import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Dictionary mapping PP_ID to file names (example data structure)
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
number_of_added_files= 0



# Path to the processed data folder
input_path = r'C:\Users\ahmed\Desktop\Masterarbeit\Test_data\processed_data2'
output_path = r'C:\Users\ahmed\Desktop\Masterarbeit\Weather_Year_Files'

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)
logging.info(f"Output directory set to: {output_path}")

# Weather years to iterate over
weather_years = list(range(1985, 1986))  # From 1982 to 2019

# Loop through each weather year
for year in weather_years:
    # Initialize an empty DataFrame with required columns
    pp_non_ava = pd.DataFrame(columns=['VARID', 'KWID', 'PKTNR', 'REVNV', 'RID'])
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
                    number_of_added_files = number_of_added_files + 1
                else:
                    logging.warning(f"File {file_path} missing required columns for year {year}. Skipping.")
        else:
            logging.warning(f"No files found starting with {file_prefix} for PP_ID {pp_id}")

    # Save the DataFrame to an Excel file for this specific weather year
    output_file_path = os.path.join(output_path, f"{year}")
    os.makedirs(output_file_path, exist_ok=True)
    output_file_path = os.path.join(output_file_path, f"WeatherYear_{year}.csv")
    pp_non_ava.to_csv(output_file_path, index=False)
    logging.info(f"Created file: {output_file_path}")
    logging.info(f"Created file: {output_file_path}")
    print('number_of_added_files = ', number_of_added_files,'   Soll = 119')