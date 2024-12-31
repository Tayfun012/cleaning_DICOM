import os
import tkinter as tk
from tkinter import filedialog
import configparser
import os
from pathlib import Path
import tkinter as tk
import sys
import json

from tools.removing import *


if __name__ == '__main__':

    # --------------  Einlesen des Ordners mit Dicom Dateien --------------
    root = tk.Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Wählen Sie den Ordner aus:')
    output_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_out_Secondary_Capture_Image_Storage")
    output_folder1 = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_out_Dose_Report")
    error_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_error")
    #----------------------------------------------
    
    # Dicom Tags entfernen
    Removing.removing_tag(input_folder, output_folder,error_folder,output_folder1)
    Removing.delete_empty_folders(input_folder)


