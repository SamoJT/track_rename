from mutagen import File
from os import  path, rename, scandir
from pathlib import Path

def extract_rename(directory):
    # Takes a full path to a directory containing music files.
    # These are then checked for file type, if there is
    # 'Title' metadata available, and finally if there are any
    # forbidden file name characters. Once checks have been
    # passed the file is renamed using os module.
    
    unchanged = []
    for file in scandir(directory):
        ext = Path(file.path).suffix
        if ext not in ['.mp3', '.wav', '.flac']:
            unchanged.append(f"{file.name} due to unsupported file type.\n")
            continue
        
        meta_title = File(file, easy=True).get('title')
        if meta_title == None:
            unchanged.append(f'{file.name} due to no "Title" metadata.\n')
            continue
        
        forbidden = [' /', '/', ':', '*', '?', '"', '<', '>', '|']
        if [char for char in forbidden if char in meta_title[0]]:
            unchanged.append(f"{file.name} due to forbidden characters.\n")
            continue
        
        print(f'Old: {file.name}')
        print(f'New: {meta_title[0]}{ext}\n')
        rename(file.path, f'{directory}{meta_title[0]}{ext}')
    return unchanged

def main():
    directory = "C:/Users/Sam/Music/D&B/VA - Planet V Drum And Bass Vol. 1/"
    unchanged = extract_rename(directory)
    
    if unchanged != None:
        print("The following were not renamed:")
        for item in unchanged:
            print(item)
               
if __name__ == '__main__':
    main()