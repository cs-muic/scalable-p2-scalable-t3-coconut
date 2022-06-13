import os
from pathlib import Path


pwd = os.getcwd()
directory = f'{pwd}/input-vdo'

# iterate over files in
# that directory
print(directory)
files = Path(directory).glob('*')
for file in files:
    print(str(file).split("/")[-1]) 