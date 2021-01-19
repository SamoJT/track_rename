from mutagen import File
from os import  path, rename, scandir

def extract_rename(directory):
    unchanged = []
    for file in scandir(directory):            
        if file.path.endswith('mp3') or file.path.endswith('wav') or file.path.endswith('flac'):
            meta_title = File(file, easy=True).get('title')
            if meta_title != None:
                forbidden = [' /', '/', ':', '*', '?', '"', '<', '>', '|']
                if [char for char in forbidden if char in meta_title[0]]:
                    unchanged.append(f"{file.name} due to forbidden characters.\n")
                else:
                    print(f'Old: {file.name}')
                    ext = path.splitext(file)
                    print(f'New: {meta_title[0]}{ext[1]}\n')
                    rename(file.path, f'{directory}{meta_title[0]}{ext[1]}')
            else:
                unchanged.append(f'{file.name} due to no "Title" metadata.\n')
        else:
            unchanged.append(f"{file.name} due to unsupported file type.\n")
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