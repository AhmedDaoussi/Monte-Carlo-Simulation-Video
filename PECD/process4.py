import pandas as pd

def create_special_input_files(file_path, countries, technologies, weights_by_tech, output_file_template):
    global columns_to_weight

    # Iterate through each technology
    for tech, weights in weights_by_tech.items():
        data_list = []

        # Ensure the specified technology exists in the technologies list
        if tech not in technologies:
            print(f"Technology '{tech}' not in specified technologies list. Skipping.")
            continue

        # Iterate through each country for the specific technology
        for country, weight in zip(countries, weights):
            # Construct the filename pattern to load
            file_pattern = f"{file_path}/{tech}_2033_{country}_shape_a.xlsx"

            # Load the Excel file if it exists
            try:
                df = pd.read_excel(file_pattern)

                # Apply the weight only to columns from '1982' to '2019'
                columns_to_weight = [col for col in df.columns[2:]]
                df_weighted = df.copy()
                df_weighted[columns_to_weight] = df[columns_to_weight] * weight  # Apply weight only to specified columns
                data_list.append(df_weighted)

            except FileNotFoundError:
                print(f"File not found: {file_pattern}")
                continue

        # Combine all weighted data for this technology
        if data_list:
            combined_data = pd.concat(data_list)

            # Group by 'Date' and 'Hour' columns and sum the weighted columns
            combined_data = combined_data.groupby(['Date', 'Hour'])[columns_to_weight].sum().reset_index()

            # Format output file based on the template
            output_file = output_file_template.format(file_path=file_path, tech=tech, country='NO')
            combined_data.to_excel(output_file, index=False, engine='openpyxl')

            print(f"Created file: {output_file}")

# Example of how to call this function
file_path = r"C:\\Users\\ahmed\\Desktop\\Masterarbeit\\Test_data\\processed_data2"
countries = ['NOS0', 'NON1', 'NOM1']  # List of countries
technologies = ['wind_off']  # List of technologies
weights_by_tech = {

    'wind_off': [0.333, 0.333, 0.333]

}
output_file_template = "{file_path}/{tech}_2033_{country}_shape_a.xlsx"

create_special_input_files(file_path, countries, technologies, weights_by_tech, output_file_template)
