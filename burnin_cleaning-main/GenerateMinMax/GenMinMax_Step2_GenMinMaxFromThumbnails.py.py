import numpy as np
from PIL import Image
import os
from multiprocessing import Pool
from datetime import datetime, timezone

import time
import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path

def list_files_recursive(directory):
    file_list = []
    for root, dirs, files in os.walk(directory, topdown=False, followlinks=True):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def create_directories_for_file(file_path):
    # Extrahiere den Verzeichnispfad aus dem Dateipfad
    directory = os.path.dirname(file_path)
    
    # Erstelle das Verzeichnis (inkl. aller Zwischenverzeichnisse), falls es nicht existiert
    if not os.path.exists(directory):
        os.makedirs(directory)


def max_projection_from_stack(image_folder, output_filepath,errorFile):
    """
    Compute the maximum projection of a stack of images without loading the full stack into memory.

    Parameters:
        image_folder (str): Path to the folder containing PNG images.
        output_path (str): Path to save the resulting maximum projection image.

    Returns:
        None
    """
    # Initialize variables
    max_image = None
    print("Start Processing Folder :  %s" % (image_folder))
    FileList=list_files_recursive(image_folder)
    print("--> File %i at  Folder :  %s" % (len(FileList),image_folder))
    # Iterate through all PNG files in the folder
    for filename in FileList:
        if filename.endswith(".png"):
            file_path =  filename
            # Load the current image as a NumPy array
            current_image = np.array(Image.open(file_path))
            
            # Initialize max_image with the first image
            if max_image is None:
                max_image = current_image
            else:
                # Update max_image with the element-wise maximum
                try:
                    max_image = np.maximum(max_image, current_image)
                except:
                    print("Error using File: %s\n" % file_path)
                    with open(errorFile, "a") as file:
                        # Write the string "New" followed by a newline character
                        file.write("Error using File: %s\n" % file_path)

    # Save the resulting maximum projection as a new image
    if max_image is not None:
        result_image = Image.fromarray(max_image)
        create_directories_for_file(output_filepath)
        result_image.save(output_filepath)
        #print(f"Maximum projection saved to {output_filepath}")
        print("Finish: Saving %s for Processing Folder  %s" % (output_filepath, image_folder))
    else:
        print("No images found in the specified folder.")




# Example usage
#image_folder = "path/to/your/image/folder"
#output_path = "path/to/save/max_projection.png"
#max_projection_from_stack(image_folder, output_path)
def check_cli_argument():
    return len(sys.argv) > 1

# Hauptlogik
if check_cli_argument():
    # Wenn ein Argument übergeben wurde, verwenden wir es
    image_folder = sys.argv[1]
    print(f"Verwendetes Verzeichnis: {image_folder}")
else:
    # Wenn kein Argument übergeben wurde, öffne eine GUI zur Verzeichnisauswahl
    print("Kein CLI-Argument gefunden. Bitte wählen Sie ein Verzeichnis aus.")
    
    # GUI initialisieren
    root = Tk()
    root.withdraw()  # Das Hauptfenster ausblenden
    
    # Verzeichnis auswählen
    image_folder = askdirectory(title="Wählen Sie ein Verzeichnis", initialdir="./MinMax/PNG_Out")
    
    if image_folder:
        print(f"Ausgewähltes Verzeichnis: {image_folder}")
    else:
        print("Kein Verzeichnis ausgewählt.")


# Additional arguments for the function
path = Path(image_folder)
project=path.name
print("BaseName:%s"%(image_folder))
#image_folder            = ("./MinMax/PNG_Out/%s" % project)
#SourceFolder    = "Argument2"
output_filepath         = ("./MinMax/MinMax_Out/%s" % project)
# Prepare arguments as tuples for starmap
utc_time = datetime.now(timezone.utc)
utc_time_str = utc_time.strftime("%Y%m%d%H%M%S%Z")

errorFile="GenMinMax_Step1_error_Pro%s-T%s.txt" % (project ,utc_time_str)
errorFile=os.path.join(output_filepath,errorFile)
print("output_filepath:%s"%(output_filepath))


tasks = [(os.path.join(image_folder,fileDir),  os.path.join(output_filepath, f"{fileDir}.png"), errorFile) for fileDir in os.listdir(image_folder)]

#start_time = time.perf_counter()
with Pool(processes=10) as pool:
    pool.starmap(max_projection_from_stack, tasks)

