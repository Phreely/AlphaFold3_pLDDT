"""
place this file on AlphaFold3 predicted directory
In case of using AlphaFold2 replace ('atom_plddts') with ('plddt') in line 10
"""
import json
import os
import numpy as np
from collections import defaultdict

# In case of using AlphaFold2 replace ('atom_plddts') with ('plddt')
FindFor = 'atom_plddts'

def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def rename_files_by_rank(files, rankings):
    for rank, file_path in enumerate(rankings, start=1):
        new_file_name = os.path.join(os.path.dirname(file_path), f"{os.path.basename(file_path).split('.')[0]}_rank{rank}.json")
        os.rename(file_path, new_file_name)

current_directory = os.path.dirname(os.path.abspath(__file__))
files = find_json_files(current_directory)

avg_scores = defaultdict(list)

for file in files:
    with open(file) as f:
        d = json.load(f)
        if FindFor in d:
            avg = np.array(d[FindFor]).mean()
            avg_scores[avg].append(file)
            print(file, 'Average pLDDT: ', avg)

# Sort the average scores in descending order and rename the files
rankings = []
for avg, files in sorted(avg_scores.items(), reverse=True):
    rankings.extend(files)

rename_files_by_rank(files, rankings)
