#!/usr/bin/env python3

import argparse
import os
from concurrent.futures import ProcessPoolExecutor


# csv files are in the format: 
# NAME    CLIP_ID	START_SECOND STAR_MSECOND	ENDSECOND    END_MSECOND
# 2017-07-21_1000_US_MSNBC_Morning_Joe.txt	t__5c626584_6dfb_11e7_8c64_089e01ba0326	204	61	204	79
# /db/tv/2016/2016-01/2016-01-01/2016-01-01_0300_US_KCBS_The_Insider.txt
# curl_command="curl -L -o \"NAME\" \"https://gallo.case.edu/cgi-bin/snippets/newsscape_mp4_snippet.cgi?file=${CLIP_ID}&start=${STAR}&end=${END}\""


# download_clip downloads a clip given a line from the csv file
def download_clip(line, searchterm, output_dir, offset):
    # split the line
    line = line.strip().split('\t')
    # remove .txt from the name
    name = line[0].replace('.txt', '')
    # take only the name of the file deleting the path if exists
    name = name.split('/')[-1]  
    clip_id = line[1]
    start_sec_orig = int(line[2])
    start_msec_orig = int(line[3])
    end_sec_orig = int(line[4]) 
    end_msec_orig = int(line[5])
    

    if name.startswith('2017'):
        print(200*'*')
        divisor = 1000
        print(f'DIVISOR: {divisor}')
    else:
        print(200*'*')
        divisor = 100
        print(f'DIVISOR: {divisor}')

    # start
    start = float(start_sec_orig) + float(start_msec_orig)/divisor - float(offset)
    # start with only 3 decimals    
    start = round(start, 3)
    # end with only 3 decimals
    end = float(end_sec_orig) + float(end_msec_orig)/divisor + float(offset)
    end = round(end, 3)

    # name is name_searchterm_start_end.mp4
    name = f'{name}_{start}_{end}_{searchterm}.mp4'

    curl_command = f'curl -L -o "{output_dir}/{name}" "https://gallo.case.edu/cgi-bin/snippets/newsscape_mp4_snippet.cgi?file={clip_id}&start={start}&end={end}"'
    os.system(curl_command)
    print(curl_command)
    print(f'Downloading {name} from {start} to {end}')

# download_clips downloads all the clips in the csv file concurrently
def download_clips(csv_file, searchterm, output_dir, offset, concurrency=5):
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        with ProcessPoolExecutor(max_workers = concurrency) as executor:
            futures = [executor.submit(download_clip, line, searchterm, output_dir, offset) for line in lines]
            for future in futures:
                future.result()  # Wait for all futures to complete


def main():
    parser = argparse.ArgumentParser(description="Download clips from gallo given a csv file of this format: 2017-07-21_1000_US_MSNBC_Morning_Joe.txt t__5c626584_6dfb_11e7_8c64_089e01ba0326    204    61    204    7")
    parser.add_argument('--csv_file', help='csv file with the clips to download')
    parser.add_argument('--searchterm', help='search term to add to the name of the clips')
    parser.add_argument('--offset', help='offset to add to the start and end times', default=2.5)
    parser.add_argument('--output_dir', help='output directory to save the clips')
    parser.add_argument('--concurrency', help='number of concurrent downloads', default=5)
    args = parser.parse_args()

    # Check if the csv file exists
    if not args.csv_file:
        print('Please provide a csv file with the clips to download')
        return

    # search term only with letters and numbers
    if not args.searchterm:
        print('Please provide a search term to add to the name of the clips')
        return
    
    # search term only with letters and numbers
    if not args.searchterm.isalnum():
        print('Search term can only contain letters and numbers')
        return
    
    # Check if the output directory exists.
    if not args.output_dir:
        print('Please provide an output directory to save the clips')
        return
    
    # create the output directory if it does not exist
    os.makedirs(args.output_dir, exist_ok=True)

    # check concurrency is a number
    try:
        args.concurrency = int(args.concurrency)
    except:
        print('Concurrency must be a number')
        return

    download_clips(args.csv_file, args.searchterm, args.output_dir, args.offset)


if __name__ == '__main__':
    main()

