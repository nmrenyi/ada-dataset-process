# external sort from https://chatgpt.com/share/672c7f41-0a20-8010-bbc5-126cd0db168b
# idea ref: https://stackoverflow.com/questions/4358087/sort-with-the-limited-memory

import os
import json
import heapq
import sys
import argparse

def chunk_sort(input_file, chunk_size, temp_dir="temp_chunks"):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    chunks = []
    with open(input_file, 'r') as infile:
        current_chunk = []
        no_dislike_count_lines = 0
        no_like_count_lines = 0
        for line in infile:
            data = json.loads(line)
            if 'dislike_count' not in data or not data['dislike_count']:
                no_dislike_count_lines += 1
                continue
            if 'like_count' not in data or not data['like_count']:
                no_like_count_lines += 1
                continue
            current_chunk.append(data)
            if len(current_chunk) * len(line) >= chunk_size:
                # Sort by 'dislike_count' in descending order
                current_chunk.sort(key=lambda x: x['dislike_count'], reverse=True)
                chunk_file = os.path.join(temp_dir, f"chunk_{len(chunks)}.jsonl")
                with open(chunk_file, 'w') as outfile:
                    for item in current_chunk:
                        outfile.write(json.dumps(item) + '\n')
                chunks.append(chunk_file)
                print(f"len(Chunk {len(chunks)}) = {len(current_chunk)} ,\
                      {no_dislike_count_lines} lines no 'dislike_count', ({no_dislike_count_lines / len(current_chunk):.3f})\
                      and {no_like_count_lines} lines no 'like_count', ({no_like_count_lines / len(current_chunk):.3f})")
                current_chunk = []
                no_dislike_count_lines = 0
                no_like_count_lines = 0

        if current_chunk:  # Sort and write the last chunk if any data is left
            current_chunk.sort(key=lambda x: x['dislike_count'], reverse=True)
            chunk_file = os.path.join(temp_dir, f"chunk_{len(chunks)}.jsonl")
            with open(chunk_file, 'w') as outfile:
                for item in current_chunk:
                    outfile.write(json.dumps(item) + '\n')
            chunks.append(chunk_file)

    return chunks

def merge_sorted_chunks(chunks, output_file):
    min_heap = []
    chunk_files = [open(chunk, 'r') for chunk in chunks]

    # Initialize heap with the first line of each file
    for i, file in enumerate(chunk_files):
        line = file.readline().strip()
        if line:
            data = json.loads(line)
            # Use negative 'dislike_count' for descending order in min-heap
            heapq.heappush(min_heap, (-data['dislike_count'], i, data))

    with open(output_file, 'w') as outfile:
        while min_heap:
            _, idx, data = heapq.heappop(min_heap)
            outfile.write(json.dumps(data) + '\n')
            next_line = chunk_files[idx].readline().strip()
            if next_line:
                next_data = json.loads(next_line)
                heapq.heappush(min_heap, (-next_data['dislike_count'], idx, next_data))

    for file in chunk_files:
        file.close()

    # Optionally, delete the temporary chunk files
    for chunk in chunks:
        os.remove(chunk)

if __name__ == "__main__":
    # use argparse to get the chunk size
    parser = argparse.ArgumentParser(description='External Sort')
    parser.add_argument('--input_file', type=str, default='./dataset/__mini__yt_metadata_en.jsonl.100k', help='Path to the large input file')
    parser.add_argument('--output_file', type=str, default='', help='Path to the output file')
    parser.add_argument('--chunk_size', type=float, default=1.0, help='Size of each chunk in bytes (default: 1 GB)')
    args = parser.parse_args()
    # print args
    print("Input file:", args.input_file)
    print("Output file:", args.output_file)
    print("Chunk size:", args.chunk_size, "GB")
    
    chunk_size = args.chunk_size * 2 ** 30
    input_file = args.input_file
    output_file = args.output_file if args.output_file else input_file.split('/')[-1].split('.')[0] + '_sorted.jsonl'

    chunks = chunk_sort(input_file, chunk_size)
    merge_sorted_chunks(chunks, output_file)

    print("Sorting completed! Sorted file:", output_file)
