import glob
import sys,os, json
import pydicom
from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path
from datetime import datetime, timezone

import os

def find_directory_by_name(start_path, target_dir_name):
    """
    Search for directories with a specific name within a folder structure.

    Args:
        start_path (str): The root directory to start the search.
        target_dir_name (str): The name of the directory to search for.
    
    Returns:
        list: A list of full paths to directories matching the target name.
    Perplexity:
        https://www.perplexity.ai/search/how-to-find-a-directory-in-a-s-CguwbTv9TJmSyzXlBzcKOA
    """
    matching_dirs = []
    
    
    #for root, dirs, _ in os.walk(start_path,recurse=False):
    for dir_name in os.listdir(start_path):
        if dir_name == target_dir_name:
            # Construct the full path to the matching directory
            matching_dirs.append(os.path.join(start_path, dir_name))

    return matching_dirs

def find_subfolder(start_path, target_folder, level=1):
    for root, dirs, _ in os.walk(start_path):
        # Calculate the depth of the current directory
        depth = root[len(start_path):].count(os.sep)
        if depth > level:  # Limit to the first two levels
            del dirs[:]  # Stop descending into deeper subdirectories
            continue
        
        # Check if the target folder is in the current directory's subdirectories
        if target_folder in dirs:
            return os.path.join(root, target_folder)
    
    return None  # Return None if the folder is not found

def find_files_by_name(filename, search_path):
    """
    Search for files with a specific name in a directory and its subdirectories.

    :param filename: Name of the file to search for.
    :param search_path: Path to the directory where the search begins.
    :return: List of full paths to the matching files.
    """
    result = []
    for root, dirs, files in os.walk(search_path):  # Recursively iterate through directories
        if filename in files:  # Check if the target file is in the current directory
            result.append(os.path.join(root, filename))  # Append the full path of the file
    return result



def split_filename(filename, delimiter):
    # Remove the file extension
    name_without_extension = filename.rsplit('.', 1)[0]
    # Split by the specified delimiter
    split_parts = name_without_extension.split(delimiter)
    return split_parts


def check_cli_argument():
    return len(sys.argv) > 1

def transform_rectangle(diagonal_point1, diagonal_point2):
    # Extract x and y coordinates
    x1, y1 = diagonal_point1
    x2, y2 = diagonal_point2
    
    # Calculate the reference point (top-left corner)
    ref_point = (max(0,min(x1, x2)), max(0,min(y1, y2)))
    
    # Calculate the width and height of the rectangle
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    
    return ref_point, (width, height)

def find_first_png(directory,fileextension):
    # Traverse the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file ends with .png
            if file.lower().endswith(fileextension):
                return os.path.join(root, file)
    return None  # Return None if no PNG file is found


# Hauptlogik
if check_cli_argument():
    # Wenn ein Argument übergeben wurde, verwenden wir es
    JSON_folder = sys.argv[1]
    print(f"Verwendetes Verzeichnis: {JSON_folder}")
else:
    # Wenn kein Argument übergeben wurde, öffne eine GUI zur Verzeichnisauswahl
    print("Kein CLI-Argument gefunden. Bitte wählen Sie ein Verzeichnis aus.")
    
    # GUI initialisieren
    root = Tk()
    root.withdraw()  # Das Hauptfenster ausblenden
    
    # Verzeichnis auswählen
    JSON_folder = askdirectory(title="Wählen Sie ein Verzeichnis", initialdir="./MinMax/MinMax_Out")
    
    if JSON_folder:
        print(f"Ausgewähltes Verzeichnis: {JSON_folder}")
    else:
        print("Kein Verzeichnis ausgewählt.")


# Additional arguments for the function
path = Path(JSON_folder)
project=path.name
print("BaseName:%s"%(JSON_folder))
#image_folder            = ("./MinMax/PNG_Out/%s" % project)
#SourceFolder    = "Argument2"
PNG_filpath             = ("./GenerateMinMax/MinMax/PNG_Out/%s" % project)
output_filepath         = ("./GenerateMinMax/MinMax/BlackMasks/%s" % project)
project="6825962_out"
# Prepare arguments as tuples for starmap
utc_time = datetime.now(timezone.utc)
utc_time_str = utc_time.strftime("%Y%m%d%H%M%S%Z")

errorFile="GenMinMax_Step03_error_Pro%s-T%s.txt" % (project ,utc_time_str)
errorFile=os.path.join(output_filepath,errorFile)

filelist= [file for file in os.listdir(JSON_folder) if file.endswith('.json')]
OutCTP=os.path.join(output_filepath,"CTP_"+ utc_time_str+".script")
if not os.path.exists(output_filepath):
        os.makedirs(output_filepath)


for file in filelist:
    Manufacturer, Model, Size, ValuesPerPixel = split_filename(file,'_')
    # ELT-Read LabelMe Jsons to 
    with open(os.path.join(JSON_folder,file), 'r') as file:
        data = json.load(file)
    ShapeList=[]
    for shape in data['shapes']:
        if shape['label'] == "Blacken" and shape['shape_type'] == "rectangle":
            ShapeList.append(shape["points"])
    #CTP Mask defintion https://mircwiki.rsna.org/index.php?title=The_CTP_DICOM_Pixel_Anonymizer
    ## Regionstring
    RegionString=""
    for Shape in ShapeList:
        ref_point, (width, height)=transform_rectangle(Shape[0],Shape[1])
        RegionString +=" (%i,%i,%i,%i)" % (ref_point[0],ref_point[1],width,height)
    RegionString=RegionString[1:]
    ## Signature 
    SignatureString=""
    # Identify a related DICOM File by DOCId
    base_name, _ = os.path.splitext(os.path.split(file.name)[1])
    PNGExamplesForMaxMinImg=find_directory_by_name( PNG_filpath,base_name)
    png_files = find_first_png(PNGExamplesForMaxMinImg[0],'.png')                            # glob.glob(f"{PNGExamplesForMaxMinImg[0]}/**/*.png", recursive=True)
    temp_folderpath, dumpfilename = os.path.split(png_files)            # temp_folderpath, dumpfilename = os.path.split(png_files[0])
    lowest_foldername = os.path.basename(temp_folderpath)
    #DICOMFolder=find_directory_by_name( "",lowest_foldername)
    InitDir="/home/ipoethke/projects-ICM/BDMS/Napkon/"
    
    normalized_path = os.path.normpath(temp_folderpath)
    List=normalized_path.split(os.sep)
    index_png_out = len(List) - 1 - List[::-1].index('PNG_Out')
    result_tail = List[-2:]
    matching_directories=find_subfolder(f"{InitDir}", result_tail[0], level=1)
    #DocIDFolder=find_subfolder(f"{matching_directories}", result_tail[1], level=1)
    #DCMfiles=os.listdir(DocIDFolder)

    #DCMfile=find_first_png(os.path.join(f"{InitDir}",project,result_tail[0]),'.dcm')
    #DCMfile=find_first_png(os.path.join(f"{InitDir}",project,result_tail[0]),'.dcm')# os.path.join(matching_directories,result_tail[1])
    DCMfile=find_first_png(os.path.join(f"{InitDir}",project,'/'.join(result_tail)),'.dcm')
    ds = pydicom.dcmread(DCMfile)
    Modality                = getattr(ds, 'Modality', 'N/A')
    ManufacturerModelName   = getattr(ds, 'ManufacturerModelName', 'N/A')
    Manufacturer            = getattr(ds, 'Manufacturer', 'N/A')
    Rows                    = str(getattr(ds, 'Rows', 'N/A'))
    Columns                 = str(getattr(ds, 'Columns', 'N/A'))
    SamplesPerPixel         = str(getattr(ds, 'SamplesPerPixel', 'N/A'))
    SignatureString='{ Modality.equals("%s")\n    * Manufacturer.containsIgnoreCase("%s")\n    * ManufacturerModelName.containsIgnoreCase("%s")\n    * Rows.equals("%s")\n    * Columns.equals("%s")\n    * SamplesPerPixel.equals("%s") }' %    (Modality,Manufacturer,ManufacturerModelName,Rows, Columns , SamplesPerPixel)
    print("Maskfor %s--> %s\n%s " % (file, SignatureString, RegionString))

    with open(OutCTP, "a") as file:
        # Write the string "New" followed by a newline character
        file.write(SignatureString + "\n" )
        file.write(RegionString + "\n\n" )
    



