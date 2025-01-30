import pandas as pd
import os

# Directory containing the CSV files
input_directory = "C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\raw_data\\PECD"
output_directory = "C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)


# Function to process the 'number' DataFrame
def process_number_df(df):
    # Count values that do not meet the criteria before transformations
    #non_criteria_count = df[df.columns[2:]].apply(lambda x: ((x < 0) | (x > 1)).sum()).sum()
    #nan_count = df[df.columns[2:]].isna().sum().sum()

    #print(f"Number of values not meeting the criteria: {non_criteria_count}")
    #print(f"Number of NaN values: {nan_count}")

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


# Loop through all files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        # Load the CSV file
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)

        # Split the DataFrame
        #df_stammdaten = df.head(9)
        df_number = df[10:].copy()

        # Use the row number 10 as header for the df_number
        df_number.columns = df.iloc[9]
        df_number.reset_index(drop=True, inplace=True)

        # Process the 'number' DataFrame
        df_number = process_number_df(df_number)

        # Create base names for the Excel files
        base_name = os.path.splitext(filename)[0]
        #stammdaten_name = os.path.join(output_directory, f"{base_name}_stammdaten.xlsx")
        number_name = os.path.join(output_directory, f"{base_name}_number.xlsx")

        # Save the split DataFrames as Excel files
        #df_stammdaten.to_excel(stammdaten_name, index=False)
        df_number.to_excel(number_name, index=False)

        print(f"Processed and saved {filename} as:")
        #print(f"  {stammdaten_name}")
        #print(f"  {number_name}")

print('a')

