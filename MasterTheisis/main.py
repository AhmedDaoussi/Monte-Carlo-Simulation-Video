from Evaluation import Evaluation
from Preprocess import PrepareDataBaseFiles,ProcessRawData, CreateShapeAFiles,RenameFilesNames

def main():
    #process_raw_data = ProcessRawData()
    #process_raw_data.format_and_transform_raw_data()

    #create_shape_a = CreateShapeAFiles()
    #create_shape_a.transform(source='Wind_Offshore')
    #create_shape_a.transform(source='Wind_Onshore')
    #create_shape_a.rename_shape_a_files()

    #rename = RenameFilesNames()
    #rename.rename_file_names()
    #prepare = PrepareDataBaseFiles(input_path=r'C:\Users\ahmed\Desktop\Masterarbeit2\Test_data\processed_data2'
    #                      , output_path=r'C:\Users\ahmed\Desktop\Masterarbeit\Weather_Year_Files_test',
    #                      weather_years=list(range(1993, 1994)))
    #prepare.prepare_data_base_files_1()
    evaluate = Evaluation(
        folder_path='C:/Users/ahmed/Desktop/ltmp_rech',
        weather_year=1982,
        start_year=2023,
        end_year=2050
    )
    #evaluate.compute_hr_prices()
    #result_df = evaluate.concatenate_and_process_yearly_data()

    #pivot_df = result_df.pivot_table(index='REGID', columns='JAHR', values='FINAL_MARKTPREIS', aggfunc='mean')
    #evaluate.plot_yearly_prices(result_df)
    #evaluate.plot_price_duration_curve(result_df)
    evaluate.evaluate_power_plant_files()



if __name__ == "__main__":
    main()

