from mutagen import File
from os import path, rename, scandir
from pathlib import Path

def extract_rename(directory):
    # Takes a full path to a directory containing music files.
    # These are then checked for file type, if there is
    # 'Title' metadata available, and finally if there are any
    # forbidden file name characters. Once checks have been
    # passed the file is renamed using os module.
    
    unchanged = []
    for file in scandir(directory):       
        try:
            ext = Path(file.path).suffix        
            meta_title = File(file, easy=True).get('title')
            if meta_title == None:
                unchanged.append(f'{file.name} due to no "Title" metadata.')
                continue

            print(f'Old: {file.name}')
            print(f'New: {meta_title[0]}{ext}\n')
            rename(file.path, f'{directory}{meta_title[0]}{ext}')

        except AttributeError:
            unchanged.append(f"{file.name} due to unsupported file type.")
        except FileExistsError:
            unchanged.append(f"{file.name} due to duplicate file existing.")
        except OSError:
            unchanged.append(f"{file.name} due to forbidden characters.")
        except:
            unchanged.append(f"{file.name} due to unknown - Likely a Mutagen error.")
    
    return unchanged

def main():
    directory = ""
    unchanged = extract_rename(directory)
    
    if unchanged != None:
        print("The following were not renamed:")
        for item in unchanged:
            print(item)
               
if __name__ == '__main__':
    main()