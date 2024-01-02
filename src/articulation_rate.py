import textgrid
import os
import pandas as pd
from pathlib import Path


def read_textgrid_file(path):
    """
    Reads a TextGrid file from the given path.

    Args:
    path (str): The path to the TextGrid file.

    Returns:
    textgrid.TextGrid: The TextGrid object read from the file.
    """
    # ensuring the path is a valid file
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")

    # read the TextGrid file
    tg = textgrid.TextGrid.fromFile(path)
    return tg


def count_syllables_in_interval(textgrid_obj, interval_start, interval_end):
    """
    Counts the number of syllable points within a specified time interval.

    :param textgrid_obj: A TextGrid object containing syllable points.
    :param interval_start: The start of the interval (inclusive).
    :param interval_end: The end of the interval (inclusive).
    :return: The count of syllable points within the interval.
    """
    count = 0
    for tier in textgrid_obj:
        if tier.name == 'syllables':  
            for point in tier:
                if interval_start <= point.time <= interval_end:
                    count += 1
            break
    return count


def count_pauses_in_interval(textgrid_obj, interval_start, interval_end):
    """
    Counts the number of silent intervals that are completely within a specified time interval.

    :param textgrid_obj: A TextGrid object containing intervals of silence and sounding.
    :param interval_start: The start of the interval (inclusive).
    :param interval_end: The end of the interval (inclusive).
    :return: The count of silent intervals within the interval.
    """
    pause_count = 0
    for tier in textgrid_obj:
        if tier.name == 'silences':  # Replace with the actual name of the tier containing silent intervals
            for interval in tier:
                if interval.mark == 'silent' and interval.minTime >= interval_start and interval.maxTime <= interval_end:
                    pause_count += 1
            break
    return pause_count


def calculate_pause_duration_in_interval(textgrid_obj, interval_start, interval_end):
    """
    Calculates the total duration of silent intervals within a specified time interval.

    :param textgrid_obj: A TextGrid object containing intervals of silence and sounding.
    :param interval_start: The start of the interval (inclusive).
    :param interval_end: The end of the interval (inclusive).
    :return: The total duration of silent intervals within the interval.
    """
    pause_duration = 0
    for tier in textgrid_obj:
        if tier.name == 'silences':  # Replace with the actual name of the tier containing silent intervals
            for interval in tier:
                if interval.mark == 'silent' and interval.minTime >= interval_start and interval.maxTime <= interval_end:
                    pause_duration += interval.maxTime - interval.minTime
            break
    return pause_duration


def get_textgrid(row):
    # access 'Participant' and 'Visit' from the current row
    childname = row['Participant'] # access 'Participant' from the current row
    sessionnumber = str(row['Visit']) # access 'Visit' from the current row and convert to string
    
    # define the directory path and format the textgrid file
    textgrid_dir = os.path.join(parent_dir, 'data','textgrid/')
                                    
    tg_path = f"{textgrid_dir}{childname}_Visit_{sessionnumber}.TextGrid"
    
    return tg_path


if __name__ == '__main__':
    
    current_dir = Path(__file__)  
    parent_dir = current_dir.parents[1] 
    diarization_file = os.path.join(parent_dir, 'data', 'TurnTakingData.csv')
    df = pd.read_csv(diarization_file)
    
    for index, row in df.iterrows():
        tg_path = get_textgrid(row)
        print(f"Processing: {tg_path}")
        
        if pd.isna(row['StartTimeSec']) or pd.isna(row['EndTimeSec']):
            print(f"Row {index} skipped due to missing StartTimeSec or EndTimeSec")
            continue

        # read the TextGrid file
        try:
            tg = read_textgrid_file(tg_path)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

        # extract the start and end times from the row
        start_time = row['StartTimeSec']
        end_time = row['EndTimeSec']

        # count syllables in the interval
        syllable_count = count_syllables_in_interval(tg, start_time, end_time)
        print(f"Syllable Count for Row {index}: {syllable_count}")
        # add syllable count to dataframe
        df.loc[index, 'SyllableCount'] = syllable_count

        # count pauses in the interval
        pause_count = count_pauses_in_interval(tg, start_time, end_time)
        print(f"Pause Count for Row {index}: {pause_count}")
        # add pause count to dataframe
        df.loc[index, 'PauseCount'] = pause_count

        # calculate pause duration in the interval
        pause_duration = calculate_pause_duration_in_interval(tg, start_time, end_time)
        print(f"Pause Duration for Row {index}: {pause_duration}")
        # add pause duration to dataframe
        df.loc[index, 'PauseDuration'] = pause_duration
        
    # save dataframe 
    output_csv_file = os.path.join(parent_dir, 'outputs', 'TurnTakingData_articulation.csv')
    df.to_csv(output_csv_file, index=False)
    print(f"DataFrame saved to {output_csv_file}")