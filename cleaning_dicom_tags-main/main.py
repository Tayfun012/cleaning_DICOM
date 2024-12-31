# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog
import configparser
import os
from pathlib import Path
import tkinter as tk
import sys
import json


from tools.config_parse import *
from tools.removing import *
from tools.matching import *


if __name__ == '__main__':

    # --------------  Einlesen des Ordners mit Dicom Dateien --------------
    root = tk.Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Wählen Sie den Ordner aus:')
    output_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_out")
    error_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_error")
    #----------------------------------------------


    #---------Einlesen der Config.ini -------------
    file_path = os.path.abspath(__file__)
    directory, filename = os.path.split(file_path)

    with open(directory + "/config/config.json") as f:
        config_settings=json.load(f)
    
    #config_name = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_settings["config_file"])
    pattern = re.compile(r"^(export_|suep_|hap_|pop_|)\d+$")
    #pattern = re.compile(r"^(bdms_)\d+$")
    
    # Ersetzen des ganzen Inhalts des gewünschten Tags mit *removed*
    tags_to_remove=Config_parse.parse_config_remove_tag('DICOM_TAGS','tags_to_remove',config)
    
    # Nur bestimmte Zeichenkette in den folgenden String-Tags mit *removed* entfernen
    string_in_tags_to_remove=Config_parse.parse_config_remove_tag('DICOM_TAGS','string_in_tags_to_remove',config)  

    #Welche String-Zeichenketten sollen entfernt werden?
    string_name=Config_parse.parse_config_remove_string('DICOM_TAGS','string_name',config)
    string_name=[s.encode().decode('unicode_escape') for s in string_name]
    #----------------------------------------------

    # Einlesen der Matching Tabelle für die Seriennummern 
    match_dict=Matching.read_table(config_settings["device_serial_table"])

    # Dicom Tags entfernen
    Removing.removing_tag(input_folder, output_folder,error_folder,tags_to_remove, string_in_tags_to_remove, string_name, match_dict,pattern)

