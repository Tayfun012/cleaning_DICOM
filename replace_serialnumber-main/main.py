import shutil
import pydicom
import os,re
from pathlib import Path
import pdb
import tkinter as tk
from tkinter import filedialog
#import dcm4che
import configparser
import ast
import sys
import csv
import re


matching_csv_path = sys.argv[1]
export_csv_path=sys.argv[2]

#matching_csv_path='/data01/shares/projects-ICM/BDMS/Herausgabe/Programme/production/matching_table/zoller.csv'
#export_csv_path='/data01/shares/projects-ICM/BDMS/Herausgabe/Protocoll/DIR__data01_shares_projects-ICM_BDMS_Herausgabe_Herausgabefall_010_Input_zo_part1/Data/ExportbyTag.csv'

match_dict = {}

with open(matching_csv_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        if len(row)>0:
            match_dict[row[0]] = row[1]   


# Export.csv einlesen
new_match_dict = match_dict.copy()
with open(export_csv_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        # Suche den TAG (0018, 1000). Falls existiert:
        if row[0] == '(0018, 1000)':
            # Extrahiere den Inhalt ab Spalte 4 bis zum Ende
            serial_numbers = row[3:]
            # Gehe die Seriennummern durch und füge sie zum Dictionary hinzu
            for serial_number in serial_numbers:
                # Wenn die Seriennummer nicht der folgenden regular Expression passt, überspringe sie
                if re.search(r'^[\W_]+$', serial_number):
                    continue
                else:
                    if serial_number in new_match_dict:
                        continue
                    else:
                        new_id = str(len(new_match_dict) + 1)
                        new_match_dict[serial_number] = new_id

# Dictiononary abspeichern in die csv               
with open(matching_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    for key, value in new_match_dict.items():
        writer.writerow([key, value])
