#!/usr/bin/env python3

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Run all tools to create a multimodal dataset.")
    parser.add_argument('--input', help='csv file from tabulate', required=True)
    parser.add_argument('--output_folder', help='output folder to save the dataset', required=True)
    parser.add_argument('--searchterm', help='searchterm to download the videos', required=True)
    parser.add_argument('--offset', help='offset to download the videos', required=True, type=int, default=2)
    parser.add_argument('--check_hands', help='check hands in the videos', required=False, type=bool, default=False)
    
    args = parser.parse_args()
    searchterm = args.searchterm
    offset = args.offset

    # if the input file doesn't exist exit
    if not os.path.exists(args.input):
        print('Input file doesn\'t exist.')
        return
    
    # if the output folder doesn't exist create it
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)


    # download clips
    print('Downloading clips...')
    os.system(f'python3 download_clips.py --csv_file {args.input} \
            --searchterm {searchterm} \
            --output_dir {args.output_folder}/videos/raw \
            --offset {offset}')

    # is_the_person_in_the_video ?
    print('Discarding clips with more than one person...')
    os.system(f'python3 is_there_a_person_in_the_video.py --videos_folder {args.output_folder}/videos/raw \
            --discarded_videos {args.output_folder}/videos/discarded \
            --matched_videos {args.output_folder}/videos/1_person \
            --check_hands {args.check_hands}')
    
    # run openpose
    print('Running OpenPose and dfMaker..., this may take a while')
    os.system(f'python3 argos.py --videos_folder {args.output_folder}/videos/1_person \
            --output_folder {args.output_folder} \
            --openpose_path /opt/openpose \
            --face_hands True \
            --skeletons True')
    
    # run speech analysis
    print('Running speech analysis...')
    os.system(f'python3 ecos.py --input_folder {args.output_folder} --n_persons 1')

    # run whisperX
    print('Running whisper and framer...')
    os.system(f'python3 apate.py --input_folder {args.output_folder} --n_persons 1')
    
    # Combine all the data and generate the dataset 
    print('Combining all the data and generating the dataset...')
    os.system(f'python3 hefesto.py --input_folder {args.output_folder} --n_persons 1 --db_name {args.output_folder}/dataset.duckdb')

    # move good videos to a folder 
    # loop over the parque files in OUTPUT_FOLDER/dataset/N_PERSONS/parquet_files/*
    # copy the corresponding video to OUTPUT_FOLDER/videos/good/
    # OUTPUT_FOLDER/videos/raw/VIDEO.mp4 -> OUTPUT_FOLDER/videos/good/VIDEO.mp4
    # create a folder for each video in OUTPUT_FOLDER/videos/good/VIDEO_NAME/ 
    os.makedirs(os.path.join(args.output_folder, 'videos/good'), exist_ok=True)
    for parquet_file in os.listdir(os.path.join(args.output_folder, 'dataset', '1_persons', 'parquet_files')):
        if parquet_file.endswith('.parquet'):
            video_name = parquet_file.replace('.parquet', '.mp4')
            os.system(f'mv {os.path.join(args.output_folder, "videos/raw", video_name)} {os.path.join(args.output_folder, "videos/good", video_name)}')


if __name__ == '__main__':
    main()

