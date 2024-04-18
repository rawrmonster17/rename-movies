#!/usr/bin/env python3

import re
import argparse
import os

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='Specify a directory path')
parser.add_argument('--pretend', action='store_true', help='Run the script in pretend mode')
args = parser.parse_args()

# Use the files in the specified directory if a path is given, otherwise use the folder_names list
if args.path:
    folder_names = [name for name in os.listdir(args.path) if name != 'lost+found']
else:
    folder_names = [
        # Movies that the names are scrambled but should not change the way that regex works on it.
        'Hqitmf Ao Lmt Zpa (1986) [BluRay] [1080p] [YXV.RP]',
        'Gqfs Npv Dech (2014) 720p BluRay k265 HEVC FVTJBR',
        'Jtukv Opxyjg Rqyuvq (2004) [BluRay] [1080p] [YXV.RP]',
        'Myeuvbqïß Qyrnwnhtt Djmtm Qf Lmt Wbdj (1984) [720p] [BluRay] [YXV.YB]',
        'Nbvofjdsä Pg Lmt Cawmoz Pg Lmt Yqpg (1988) (1080p BluRay k265 HEVC 10vjv FBDC3 2.0 Qmdjptvnfz Hctsnuvf)',
        'Pumisï Qqml (1994) (1080p BluRay k265 HEVC 10vjv FBDC3 2.0 Qmdjptvnfz Hctsnuvf)',
        'Qqpd (2008) [BluRay] [1080p] [YXV.RP]',
        'Qummrvsrj Npqutqlrh (1997) [BluRay] [1080p] [YXV.RP]',
        'Lmt.Vqwbzbo.2011.DVDRip.FjvQ-RCF',
        'Xqfvo Qjstu Bfj Ykzfq (2014) [1080p] [BluRay] [5.1] [YXV.YB]',
        'Hqitmf Ao Lmt Zpa (1986) [BluRay] [1080p] [YXV.RP]',
        'Obwm_Jqfcvteq(1991)',
        'Qivsxvq_qf_lmt_Bzspqrsmznl_Dggd_Mfv_Udbb_Ppif_2017',
        'Jtukr Lqbxog Qyrnwnht 2004 720p BluRay k264-x0r'
    ]

# Lists to store the results of processing the folder names
matched = []  # Folders that matched the regular expression and will be renamed
unmatched = []  # Folders that didn't match the regular expression
wont_touch = []  # Folders that already have the desired format

# Process each folder name
for folder_name in folder_names:
    try:
        match = re.search(r"(.*?)[\s\._]*(?:\((\d{4})\)|(\d{4}))(?:\D|$)(.*)?", folder_name)
        if match:
            movie_name = match.group(1).replace('.', ' ').strip().replace(' ', '_')
            year = match.group(2) if match.group(2) else match.group(3)
            new_name = f"{movie_name}({year})"
            # If the folder name already matches the desired pattern, add it to the wont_touch list
            if folder_name == new_name:
                wont_touch.append(folder_name)
                continue
            # Include the entire original name, but replace spaces with underscores
            matched.append((folder_name, new_name))
        else:
            unmatched.append(folder_name)
    except Exception as e:
        print(f"Error processing folder name {folder_name}: {e}")

print("Matched:")
for old_name, new_name in matched:
    try:
        verb = "test_move" if args.pretend else "Renaming"
        print(f"{verb} {old_name} to {new_name}")
        if args.path and not args.pretend:
            os.rename(os.path.join(args.path, old_name), os.path.join(args.path, new_name))
    except Exception as e:
        print(f"Error {verb.lower()} {old_name} to {new_name}: {e}")

print("\nUnmatched:")
for folder_name in unmatched:
    print(f"No match found for: {folder_name}")

print("\nWon't touch:")
for folder_name in wont_touch:
    print(f"Already in desired format: {folder_name}")

# Usage
# ./test.py --pretend -p ~/path/to/movies

# After renaming the folders...
for _, new_name in matched + [(name, name) for name in wont_touch]:
    try:
        # Get a list of all files in the folder
        files = os.listdir(os.path.join(args.path, new_name))
        # Filter the list to only include movie and subtitle files
        files = [f for f in files if f.endswith(('.avi', '.mkv', '.mp4', '.srt', '.sub'))]
        # Get a list of all movie files
        movie_files = [f for f in files if f.endswith(('.avi', '.mkv', '.mp4'))]
        # Check if there are any movie files
        if movie_files:
            # Find the largest movie file
            largest_movie_file = max(movie_files, key=lambda f: os.path.getsize(os.path.join(args.path, new_name, f)))
            # Rename the largest movie file and any subtitle files
            for file in files:
                extension = os.path.splitext(file)[1]
                if args.pretend:
                    print(f"Would rename {file} to {new_name + extension}")
                else:
                    os.rename(os.path.join(args.path, new_name, file), os.path.join(args.path, new_name, new_name + extension))
        else:
            print(f"No movie files found in {new_name}")
    except Exception as e:
        print(f"Error renaming files in {new_name}: {e}")