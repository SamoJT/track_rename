from mutagen import File
from os import path, rename, scandir, walk
from pathlib import Path
from platform import system

def extract_rename(directory, sl):
    # Takes a full path to a directory containing music files.
    # These are then checked for file type, if there is
    # 'Title' metadata available, and finally if there are any
    # forbidden file name characters. Once checks have been
    # passed the file is renamed using os module.

    unchanged = [[], [], [], [], []]
    for root, dirs, files in walk(directory):
        for name in files:
            full_path = path.join(root, name)
            try:
                ext = Path(full_path).suffix
                meta_title = File(full_path, easy=True).get('title')
                print(f'Old: {name}')
                print(f'New: {meta_title[0]}{ext}\n')
                rename(full_path, f'{root}{sl}{meta_title[0]}{ext}')

            except AttributeError:
                unchanged[0].append(f"UNSUPPORTED FILE TYPE: {ext} -- {name}")
            except TypeError:
                unchanged[1].append(f'NO TITLE METADATA: {name}')
            except FileExistsError:
                unchanged[2].append(f"DUPLICATE FILE EXISTS: {name}")
            except OSError:
                unchanged[3].append(f"RESTRICTED CHARACTERS: {meta_title[0]}")
            except:
                unchanged[4].append(f"UNKNOWN ERROR: {name} ")

    return unchanged

def main():
    directory = "C:\\Users\\Sam\\Music\\D&B\\"
    if system() == 'Windows':
        sl = '\\'
    elif system() == 'Linux':
        sl = '/'
    else:
        return "Unable to determine OS."
    
    unchanged = extract_rename(directory, sl)
    
    if unchanged != None:
        print("The following were not renamed:")
        for exception in unchanged:
            for error in exception:
                print(error)
    return

if __name__ == '__main__':
    main()