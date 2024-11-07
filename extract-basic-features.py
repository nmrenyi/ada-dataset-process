import os
import json
import pandas as pd
import argparse
if __name__ == '__main__':
    features_dict = {
        'categories': [],
        'upload_date': [],
        'crawl_date': [],
        'like_count': [],
        'dislike_count': [],
        'view_count': [],
        'display_id': [],
        'channel_id': []
    }
    index = 0
    parser = argparse.ArgumentParser(description='Extract categories and year from yt_metadata_en.jsonl')
    parser.add_argument('--input_file', type=str, default='./dataset/__mini__yt_metadata_en.jsonl.100k', help='Path to the large input file')
    parser.add_argument('--output_file', type=str, default='', help='Path to the output file)')
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file if args.output_file else input_file.replace('.jsonl', '_basic.csv')

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            for key in features_dict.keys():
                if key == 'crawl_date' or key == 'upload_date':
                    features_dict[key].append(data[key].split('-')[0])
                else:
                    features_dict[key].append(data[key])
            if index % 1000000 == 0:
                print(f"Processing line {index}")
            index += 1
    pd.DataFrame(features_dict).to_csv(output_file, index=False, sep='\t')
