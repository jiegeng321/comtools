import os
from tqdm import tqdm

rename_path = 'prerename_files2'

list_path_real = os.listdir(rename_path)
for i in tqdm(range(0, len(list_path_real))):
    path_real = os.path.join(rename_path, list_path_real[i])
    os.rename(path_real,os.path.join(rename_path, 'red_copy_%d.jpg'%i))

