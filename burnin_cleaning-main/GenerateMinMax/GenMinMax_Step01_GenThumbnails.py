import pydicom
import numpy as np
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_modality_lut
from multiprocessing import Pool
from datetime import datetime, timezone

import time
import os

import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory


#Implicit VR Little Endian (UID: 1.2.840.10008.1.2): The default transfer syntax for DICOM.
#Explicit VR Little Endian (UID: 1.2.840.10008.1.2.1).
#Explicit VR Big Endian (UID: 1.2.840.10008.1.2.2).
#
#The code will not work for compressed transfer syntaxes unless additional libraries or plugins are used to handle the decompression. Examples of unsupported compressed transfer syntaxes include:
#JPEG Lossless (UID: 1.2.840.10008.1.2.4.70).
#JPEG 2000 (UIDs: 1.2.840.10008.1.2.4.90 and 1.2.840.10008.1.2.4.91).
#RLE Lossless (UID: 1.2.840.10008.1.2.5).

def GetSavePathFile(SourceFolder, OutBase,file_path,ds):
    
    def replace_source_path(full_path, source_path, target_path):
        # Ensure paths are normalized for consistent comparison
        full_path = os.path.normpath(full_path)
        source_path = os.path.normpath(source_path)
        target_path = os.path.normpath(target_path)
        
        # Replace the source path with the target path
        if full_path.startswith(source_path):
            new_path = full_path.replace(source_path, target_path, 1)
            return new_path
        else:
            raise ValueError("The source path is not part of the full path.")
    def add_subfolder(path, subfolder_name):
        # Join the existing path with the new subfolder name
        new_path = os.path.join(path, subfolder_name)
        return new_path
    
    def replace_extension(file_path, new_extension):
        base_name, _ = os.path.splitext(file_path)
        return f"{base_name}.{new_extension}"

    # Extract desired metadata
    ManufacturerModelName   = getattr(ds, 'ManufacturerModelName', 'N/A').replace(" ","")
    Manufacturer            = getattr(ds, 'Manufacturer', 'N/A').replace(" ","")
    Rows                    = str(getattr(ds, 'Rows', 'N/A')).replace(" ","")
    Columns                 = str(getattr(ds, 'Columns', 'N/A')).replace(" ","")
    SamplesPerPixel         = str(getattr(ds, 'SamplesPerPixel', 'N/A')).replace(" ","")
    TargetFile=replace_source_path(file_path, SourceFolder, add_subfolder(OutBase,("%s_%s_%sx%s_%s" % (Manufacturer,ManufacturerModelName,Rows,Columns,SamplesPerPixel))))
    TargetFile=replace_extension(TargetFile,'png')
    head,tail = os.path.split(TargetFile)
    os.makedirs(head, exist_ok=True)
    return TargetFile

def dicom_to_png(dicom_file, output_file, SourceFolder, OutBase,errorFile):
    try:
        # Read the DICOM file
        ds = pydicom.dcmread(dicom_file)
        pixel_array = apply_modality_lut(ds.pixel_array, ds)
        if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
            single_frame =pixel_array[0]
        else:
            single_frame = pixel_array
        # Extract pixel array
        #pixel_array = ds.pixel_array
        
        # Normalize pixel values to 0-255 (8-bit)
        normalized_array = ((single_frame  - np.min(single_frame )) / 
                            (np.max(single_frame ) - np.min(single_frame )) * 255).astype(np.uint8)
        
        # Convert to PIL Image and save as PNG
        img = Image.fromarray(normalized_array)
        
        ExportPath=GetSavePathFile(SourceFolder, OutBase,dicom_file,ds)
        print(ExportPath)
        img.save(ExportPath)
    except Exception as e:
        print("Error using File: %s\n" % dicom_file)
        with open(errorFile, "a") as file:
            # Write the string "New" followed by a newline character
            file.write("Error using File: %s\n" % dicom_file)
        


def list_files_recursive(directory):
    file_list = []
    for root, dirs, files in os.walk(directory, topdown=False, followlinks=True):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

#SourceFolder="../../../../../Napkon/6825960_US_Link"#"../Example/US_Package"


def check_cli_argument():
    return len(sys.argv) > 1

# Hauptlogik
if check_cli_argument():
    # Wenn ein Argument übergeben wurde, verwenden wir es
    SourceFolder = sys.argv[1]
    print(f"Verwendetes Verzeichnis: {SourceFolder}")
else:
    # Wenn kein Argument übergeben wurde, öffne eine GUI zur Verzeichnisauswahl
    print("Kein CLI-Argument gefunden. Bitte wählen Sie ein Verzeichnis aus.")
    
    # GUI initialisieren
    root = Tk()
    root.withdraw()  # Das Hauptfenster ausblenden
    
    # Verzeichnis auswählen
    SourceFolder = askdirectory(title="Wählen Sie ein Verzeichnis")
    
    if SourceFolder:
        print(f"Ausgewähltes Verzeichnis: {SourceFolder}")
    else:
        print("Kein Verzeichnis ausgewählt.")




LastFolder=os.path.basename(os.path.dirname(os.path.normpath(SourceFolder)))
OutBase=("./MinMax/PNG_Out/%s" % (LastFolder))

utc_time = datetime.now(timezone.utc)
utc_time_str = utc_time.strftime("%Y%m%d%H%M%S%Z")
errorFile="GenMinMax_Step1_error_Pro%s-T%s.txt" % (LastFolder ,utc_time_str)
errorFile=os.path.join(OutBase,errorFile)



ListofFiles=list_files_recursive(SourceFolder)

# Additional arguments for the function
output          = "notapplicable"
#SourceFolder    = "Argument2"
#OutBase         = ""
# Prepare arguments as tuples for starmap
tasks = [(file, "output.png" ,SourceFolder, OutBase,errorFile) for file in ListofFiles]


start_time = time.perf_counter()
with Pool(processes=20) as pool:
    pool.starmap(dicom_to_png, tasks)


#for ListofFile in ListofFiles:
    # Example usage
    #dicom_to_png("../Example/US_Package/7297528/1303643.dcm", "output.png", SourceFolder, OutBase)
    #dicom_to_png(ListofFile, "output.png", SourceFolder, OutBase)

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
