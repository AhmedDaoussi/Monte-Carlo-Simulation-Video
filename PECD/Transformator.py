import pandas as pd
import os
import numpy as np

# Directory containing the Excel files
input_directory = "C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data"
output_directory = "C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\transformed_data"
# Dictionary Files
dic_offshore = pd.read_excel("C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\raw_data\\shpab_offshore.xlsx")
dic_onshore = pd.read_excel("C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\raw_data\\shpab_onshore.xlsx")



def find_closest_key(lookup_value, value_map):
    """Find the closest key in the dictionary to the lookup_value."""
    keys = np.array(list(value_map.keys()))
    closest_key = keys[np.argmin(np.abs(keys - lookup_value))]
    return closest_key


def transform(source, input_directory, output_directory):
    # Loop through all files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith("_number.xlsx") and source in filename:
            # Load the Excel file
            file_path = os.path.join(input_directory, filename)
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
                df[column] = df[column].apply(lambda x: value_map[find_closest_key(x, value_map)])

            base_name = os.path.splitext(filename)[0]
            output_file_path = os.path.join(output_directory, base_name + ".xlsx")

            # Save the transformed DataFrame as an Excel file
            df.to_excel(output_file_path, index=False)

            print(f"Transfor and saved {filename} as {output_file_path}")




# Execute the transformation
transform(source='Wind_Onshore', input_directory=input_directory, output_directory=output_directory)
transform(source='Wind_Offshore', input_directory=input_directory, output_directory=output_directory)
print('Transformation complete:')
