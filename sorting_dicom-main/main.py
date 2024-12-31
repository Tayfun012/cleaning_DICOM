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
    output_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_out")
    error_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_error")
    #----------------------------------------------
    
    # Dicom Tags entfernen
    Removing.sortingFile(input_folder, output_folder,error_folder)

