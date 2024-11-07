import os
import json
import pandas as pd
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
    with open('dataset/yt_metadata_en_sorted_abs.jsonl', 'r') as f:
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
    pd.DataFrame(features_dict).to_csv('dataset/yt_metadata_en_sorted_abs_category_year.csv', index=False, sep='\t')
