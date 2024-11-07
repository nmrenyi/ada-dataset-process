import pandas as pd
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Extract categories and year from yt_metadata_en.jsonl')
    parser.add_argument('--relative', type=int, default=0, help='relative dislike count or not (default: 0)')
    parser.add_argument('--output_dir', type=str, default='./specified_category_year/', help='Path to the output directory')
    args = parser.parse_args()
    input_file = f'dataset/yt_metadata_en_sorted_{'rel' if args.relative else 'abs'}_category_year.csv'
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_file, sep='\t')
    print(df.info())
    print(df.head())

if __name__ == '__main__':
    main()
