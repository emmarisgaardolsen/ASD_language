from pathlib import Path
import os
import pandas as pd


def get_txt(row):
    """
    Function for fetching the correct txt file path for each row in the dataframe.
    """

    # access 'Participant' and 'Visit' from the current row
    childname = row['Participant'] # access 'Participant' from the current row
    sessionnumber = str(row['Visit']) # access 'Visit' from the current row and convert to string
    
    # define the directory paths for f0 txt files 
    freq_directory_path = os.path.join(parent_dir,'data','f0_extracted/') 
    txt_path = f"{freq_directory_path}{childname}_Visit_{sessionnumber}_f0.txt"
    
    return txt_path


if __name__ == '__main__':

    current_dir = Path(__file__)  
    parent_dir = current_dir.parents[1] 
    diarization_file = os.path.join(parent_dir, 'data', 'TurnTakingData.csv')
    df = pd.read_csv(diarization_file)      

    # loop over each row in the dataframe
    for index, row in df.iterrows():
        txt_path = get_txt(row)  
        print(f"Processing: {txt_path}") 
        
        try: 
            # read the txt file
            f0 = pd.read_csv(txt_path, sep='\t', header=0)
            
        except Exception as e:
            print(f"Could not read {txt_path}: {e}")
            continue  # skip to the next iteration if the file can't be read


        start_time = row['StartTimeSec']
        end_time = row['EndTimeSec']
        

        # filter the f0 dataframe to only include rows between start_time and end_time
        f0 = f0[(f0['time'] >= start_time) & (f0['time'] <= end_time)]
        
        # calculate the median f0
        median_f0 = f0['f0'].median()
        
        # calculate the min f0
        min_f0 = f0['f0'].min()
        
        # calculate the max f0
        max_f0 = f0['f0'].max()
        
        # calculate the IQR f0
        q1 = f0['f0'].quantile(0.25)
        q3 = f0['f0'].quantile(0.75)
        iqr = q3 - q1
        
        
        # Add the median_f0, min_f0, max_f0, and iqr to the dataframe
        df.loc[index, 'median_f0'] = median_f0
        df.loc[index, 'min_f0'] = min_f0
        df.loc[index, 'max_f0'] = max_f0
        df.loc[index, 'q1_f0'] = q1
        df.loc[index, 'q3_f0'] = q3
        df.loc[index, 'iqr_f0'] = iqr    
        
        
    # save dataframe 
    output_csv_file = os.path.join(parent_dir, 'outputs', 'TurnTakingData_f0.csv')
    df.to_csv(output_csv_file, index=False)
    print(f"DataFrame saved to {output_csv_file}")
