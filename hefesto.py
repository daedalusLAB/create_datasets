#! /usr/bin/env python3

import os
from typing import Dict, List, Any
import pandas as pd
import pyarrow.parquet as pq
import json
import duckdb
import argparse
from datetime import datetime, timezone

from datetime import timezone

def prepare_prosody_data(prosody_path: str) -> pd.DataFrame:
    """
    Load and prepare prosody data from a parquet file.

    Args:
        prosody_path (str): Path to the prosody parquet file.

    Returns:
        pd.DataFrame: Processed prosody data.
    """
    prosody_df = pq.read_table(prosody_path).to_pandas()
    prosody_reduced_df = prosody_df.iloc[::6].rename(columns={"Frame": "frame"})

    prosody_reduced_df['frame'] = prosody_reduced_df['frame'].astype(int)
    
    # Convert datetime to UTC, then remove timezone information
    if 'datetime' in prosody_reduced_df.columns:
        if prosody_reduced_df['datetime'].dt.tz:
            prosody_reduced_df['datetime'] = prosody_reduced_df['datetime'].dt.tz_convert(timezone.utc)
        prosody_reduced_df['datetime'] = prosody_reduced_df['datetime'].dt.tz_localize(None)
        
        # Ensure microsecond precision
        prosody_reduced_df['datetime'] = pd.to_datetime(prosody_reduced_df['datetime'], format='%Y-%m-%d %H:%M:%S.%f')
    
    return prosody_reduced_df

def prepare_words_data(words_path: str) -> pd.DataFrame:
    """
    Load and prepare words data from a JSON file.

    Args:
        words_path (str): Path to the words JSON file.

    Returns:
        pd.DataFrame: Processed words data.
    """
    with open(words_path, 'r') as f:
        words = json.load(f)
    
    processed_words = []
    for frame in words:
        processed_words.append({
            "frame": frame["frame_number"],
            "words": ", ".join(frame["words"]),
            "scores_w": ", ".join(map(str, frame["scores"]))
        })
    
    return pd.DataFrame(processed_words)

def prepare_pose_data(pose_path: str) -> pd.DataFrame:
    """
    Load and prepare pose data from a parquet file.

    Args:
        pose_path (str): Path to the pose parquet file.

    Returns:
        pd.DataFrame: Processed pose data.
    """
    pose_df = pq.read_table(pose_path).to_pandas()
    pose_df["frame"] += 1
    
    return pose_df

def combine_all_data(prosody_data: pd.DataFrame, words_data: pd.DataFrame, pose_data: pd.DataFrame, filename: str) -> pd.DataFrame:
    """
    Combine prosody, words, and pose data into a single DataFrame.

    Args:
        prosody_data (pd.DataFrame): Processed prosody data.
        words_data (pd.DataFrame): Processed words data.
        pose_data (pd.DataFrame): Processed pose data.
        filename (str): Name of the file being processed.

    Returns:
        pd.DataFrame: Combined data from all sources.

    Raises:
        ValueError: If there's a mismatch in row numbers between prosody and words data.
    """
    if len(prosody_data) != len(words_data):
       print(f"Mismatch in row numbers for file: {filename} in speech analysis and words data")

    combined_prosody_words = prosody_data.merge(words_data, on='frame', how='outer')

    final_combined_data = pd.merge(combined_prosody_words, pose_data, on="frame", how="outer")
    
    # Ensure datetime is in correct format
    if 'datetime' in final_combined_data.columns:
        final_combined_data['datetime'] = pd.to_datetime(final_combined_data['datetime'], format='%Y-%m-%d %H:%M:%S.%f')
    
     # Remove rows where people_id is null 
    #final_combined_data = final_combined_data[final_combined_data['people_id'].notna()]
    
    return final_combined_data

def process_single_file(parquet_file_path: str, db_file: str) -> None:
    """
    Process a single pose file path and find related files.

    Args:
        parquet_file_path (str): Path to the parquet file.
        db_file (str): Path to the DuckDB database file.
    """
    print(f"Processing file: {parquet_file_path}")

            
    # if parquet_file_path is before_2017/dataset/1_persons/parquet_files/2017-07-21_1800_US_HLN_On_the_Story_With_Erica_Hill_2880.249_2884.569_before.parquet
    # prosody_file_path is before_2017/dataset/1_persons/parquet_speech_analysis/2017-07-21_1800_US_HLN_On_the_Story_With_Erica_Hill_2880.249_2884.569_before.parquet
    prosody_file_path = parquet_file_path.replace("parquet_files", "parquet_speech_analysis")
    # words_file is before_2017/dataset/1_persons/whisperx_framer_output/2017-07-21_1800_US_HLN_On_the_Story_With_Erica_Hill_2880.249_2884.569_before.json
    words_file_path = parquet_file_path.replace("parquet_files", "whisperx_framer_output").replace(".parquet", ".json")
    prosody_data = prepare_prosody_data(prosody_file_path)
    words_data = prepare_words_data(words_file_path)
    pose_data = prepare_pose_data(parquet_file_path)
    combined_data = combine_all_data(prosody_data, words_data, pose_data, parquet_file_path)
    
    # create folder where db_file is located if it does not exist if not os.path.exists(os.path.dirname(db_file)):

    # Insert combined_data into DuckDB without writing it out to a file
    con = duckdb.connect(db_file)
    con.register("combined_data", combined_data)
    con.execute("CREATE TABLE IF NOT EXISTS multi_data AS SELECT * FROM combined_data LIMIT 0")
    con.execute("INSERT INTO multi_data SELECT * FROM combined_data")
    # delete all rows where people_id is null
    con.execute("DELETE FROM multi_data WHERE id is null")
    con.close()

def main() -> None:
    """
    Main function to parse command line arguments and process the file.
    """
    parser = argparse.ArgumentParser(description="Process multimodal data files.")
    parser.add_argument("-i", "--input_folder", type=str, required=True, help="Path to the input folder")
    parser.add_argument("-n", "--n_persons", type=str, required=True, help="Number of persons")
    parser.add_argument("-d", "--db_name", type=str, default="minos.duckdb", help="Path to DuckDB database file")

    args = parser.parse_args()
    n_persons = f"{args.n_persons}_persons"

    print(f"Input folder: {args.input_folder}")
    print(f"Number of persons: {args.n_persons}")
    print(f"DuckDB database file: {args.db_name}")

    for parquet_file in os.listdir(os.path.join(args.input_folder, "dataset", n_persons, "parquet_files")):
        if parquet_file.endswith(".parquet"):
            process_single_file(os.path.join(args.input_folder, "dataset", n_persons, "parquet_files", parquet_file), args.db_name)

if __name__ == "__main__":
    main()
