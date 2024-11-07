import pandas as pd
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Extract categories and year from yt_metadata_en.jsonl')
    parser.add_argument('--relative', type=int, default=0, help='relative dislike count or not (default: 0)')
    parser.add_argument('--output_dir', type=str, default='./specified_category_year/', help='Path to the output directory')
    args = parser.parse_args()
    input_file = f'dataset/yt_metadata_en_sorted_{'rel' if args.relative else 'abs'}_basic.csv'
    output_dir = os.path.join(args.output_dir, 'rel' if args.relative else 'abs')
    os.makedirs(output_dir, exist_ok=True)
    # print args
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Relative dislike?: {args.relative}")
    # read the input file
    print("Reading the input file...")
    df = pd.read_csv(input_file, sep='\t')
    print(df.info())
    print(df.head())
    categories = df['categories'].value_counts().index.tolist()
    upload_years = df['upload_date'].value_counts().index.tolist()
    categories.sort()
    upload_years.sort()
    for i, category in enumerate(categories):
        for year in upload_years:
            df_filtered = df[(df['categories'] == category) & (df['upload_date'] == year)]
            df_filtered.to_csv(f'{output_dir}/{category}_{year}.csv', index=False, sep='\t')
            print(f"Category: {category}, Year: {year}, Number of videos: {df_filtered.shape[0]} saved to {output_dir}/{category}_{year}.csv")
        print(f"Category {category} done, remaining {len(categories) - i - 1} categories")

if __name__ == '__main__':
    main()
