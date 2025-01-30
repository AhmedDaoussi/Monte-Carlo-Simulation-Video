from decimal import Decimal
import pandas as pd
import os
import numpy as np


def process_number_df(df):
    """
    Processes the 'number' DataFrame using Decimal for high precision.
    """
    # Convert the second column to Decimal, coercing errors
    df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce').apply(
        lambda x: Decimal(x) if pd.notna(x) else x)

    # Iterate through columns starting from the third one
    for col in df.columns[2:]:
        df[col] = df[col].apply(lambda x: Decimal(x) if pd.notna(x) else x)
        # Find indices where values are out of expected range and adjust
        indices = df.index[(df[col] < Decimal('0')) | (df[col] > Decimal('1'))].tolist()
        for i in indices:
            if 0 < i < len(df) - 1:
                df.at[i, col] = (df.at[i - 1, col] + df.at[i + 1, col]) / Decimal('2')

        # Apply transformation value = 1 - value
        df[col] = df[col].apply(lambda x: Decimal('1') - x)

        # Optionally, round to a desired number of decimal places
        df[col] = df[col].apply(lambda x: x.quantize(Decimal('.0001')))

    return df


class Preprocess:
    def __init__(self, input_directory, output_directory, dic_offshore, dic_onshore):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.dic_offshore = dic_offshore
        self.dic_onshore = dic_onshore

        # Ensure the output directory exists
        # os.makedirs(self.output_directory, exist_ok=True)

    def find_closest_key(self,lookup_value, value_map):
        """Find the closest key in the dictionary to the lookup_value."""
        keys = np.array(list(value_map.keys()))
        closest_key = keys[np.argmin(np.abs(keys - lookup_value))]
        return closest_key

    def process_files(self):
        """
        Loops through all CSV files in the input directory, processes them, and saves the results.
        """
        for filename in os.listdir(self.input_directory + '\\raw_data\\PECD'):
            if filename.endswith(".csv"):
                # Load the CSV file
                file_path = os.path.join(self.input_directory + '\\raw_data\\PECD', filename)
                df = pd.read_csv(file_path)

                # Split the DataFrame
                df_number = df[10:].copy()

                # Use the row number 10 as header for the df_number
                df_number.columns = df.iloc[9]
                df_number.reset_index(drop=True, inplace=True)

                # Process the 'number' DataFrame
                df_number = process_number_df(df_number)

                # Create base name for the Excel file
                base_name = os.path.splitext(filename)[0]
                number_name = os.path.join(self.output_directory + '\\processed_data', f"{base_name}_number.xlsx")

                # Save the processed DataFrame as an Excel file
                df_number.to_excel(number_name, index=False)

                print(f"Processed and saved {filename} as: {number_name}")

    def transform(self, source):
        """Transform the data based on the source and save the results."""

        if source == 'Wind_Offshore':
            trans_vecs = self.dic_offshore
        elif source == 'Wind_Onshore':
            trans_vecs = self.dic_onshore

        # Ensure the output directory exists
        transformed_data_dir = os.path.join(self.output_directory, 'transformed_data')

        # Loop through all relevant files in the directory
        for filename in os.listdir(os.path.join(self.input_directory, 'processed_data')):
            if filename.endswith("_number.xlsx") and source in filename:
                file_path = os.path.join(self.input_directory, 'processed_data', filename)
                df = pd.read_excel(file_path)

                # Prepare the transformation vectors
                value_map = trans_vecs.set_index(trans_vecs.columns[1])[trans_vecs.columns[0]].to_dict()

                # Transform the values from the third column onwards
                for column in df.columns[2:]:
                    df[column] = df[column].apply(lambda x: value_map[self.find_closest_key(x, value_map)])

                base_name = os.path.splitext(filename)[0]
                output_file_path = os.path.join(transformed_data_dir, base_name + ".xlsx")


                # Save the transformed DataFrame as an Excel file
                df.to_excel(output_file_path, index=False)

                print(f"Transformed and saved {filename} as {output_file_path}")
