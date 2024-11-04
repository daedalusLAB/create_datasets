#!/usr/bin/env python3  

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Run speech analysis on a folder of videos")
    parser.add_argument('--input_folder', help='Folder with videos and dataset', required=True)
    parser.add_argument('--n_persons', help='number of persons in the videos', required=True, type=int, default=1)
    args = parser.parse_args()

    n_persons = str(args.n_persons) + "_persons"
    
    # We are going to do speech analysis on all the videos in the videos_folder that have a corresponding parquet file in the parquets_folder in n_persons
    # so we loop over all the parquet files in n_persons and run the speech analysis on the video that is in videos_folder/raw 
    # the name of the video is the name of the parquet file without the .parquet extension .mp4
    for parquet_file in os.listdir(os.path.join(args.input_folder, "dataset", n_persons, "parquet_files")):
        print(parquet_file)
        if parquet_file.endswith(".parquet"):
            video_name = parquet_file.replace(".parquet", ".mp4")
            video_path = os.path.join(args.input_folder, "videos", "raw", video_name)
            csv_path = os.path.join("/tmp", video_name.replace(".mp4", ".csv"))
            print(f"Processing {video_path}")            
            os.system(f"python3 ./speech_analysis/speech_analysis.py --video {video_path} --csv {csv_path}")
            # create the output folder if it doesn't exist
            os.makedirs(os.path.join(args.input_folder, "dataset", n_persons, "parquet_speech_analysis"), exist_ok=True)
            os.system(f"Rscript AFEES.R {csv_path} {args.input_folder}/dataset/{n_persons}/parquet_speech_analysis/{video_name.replace('.mp4', '.parquet')}")

if __name__ == '__main__':
    main()









