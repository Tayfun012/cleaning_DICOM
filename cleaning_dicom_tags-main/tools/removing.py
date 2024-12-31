# -*- coding: utf-8 -*-
import os
import pydicom
import shutil
import re
from multiprocessing import Pool, cpu_count

class Removing:
    
    #@staticmethod
    def removing_tag(input_folder, output_folder, error_folder, tags_to_remove, string_in_tags_to_remove, string_name, match_dict,pattern):
        dicom_files = []
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".dcm"):
                    dicom_files.append((root, file))
        
        args = [(root, file, input_folder, output_folder, error_folder,tags_to_remove, string_in_tags_to_remove, string_name, match_dict, pattern) for root, file in dicom_files]
        with Pool(processes=8) as pool:
            pool.map(Removing.process_dicom_file, args) 
            
    #@staticmethod       
    def process_dicom_file(args):
        """Function to process a single DICOM file."""
        root, file, input_folder, output_folder, error_folder,tags_to_remove, string_in_tags_to_remove, string_name, match_dict, pattern = args
    
        try:
            ds = pydicom.dcmread(os.path.join(root, file), force=True)

            # Haupttags und Subtags entfernen
            Removing.remove_tags(ds, tags_to_remove, string_in_tags_to_remove, string_name, match_dict, pattern)

            # Save DICOM File
            relative_path = os.path.relpath(root, input_folder)
            out_path = os.path.join(output_folder, relative_path)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            if not os.path.exists(os.path.join(out_path, file)): 
                ds.save_as(os.path.join(out_path, file))

        # Exception, sofern ein ein Fehler passiert-> Speicher des Dicom-Files in Error Ornder
        except Exception as e:
            print("Fehler beim Lesen der DICOM-Datei:", e)
            relative_path = os.path.relpath(root, input_folder)
            out_path = os.path.join(error_folder, relative_path)
            os.makedirs(out_path, exist_ok=True)
            if not os.path.exists(os.path.join(out_path, file)): 
                shutil.copy(os.path.join(input_folder, relative_path, file), os.path.join(out_path, file))
    
    #@staticmethod
    def remove_tags(ds, tags_to_remove, string_in_tags_to_remove, string_name,match_dict, pattern):
        for elem in ds:
            if elem.VR == 'SQ':  # VR = Value Representation
                for seq_item in elem:
                    Removing.remove_tags(seq_item, tags_to_remove, string_in_tags_to_remove, string_name,match_dict,pattern)
            
            #Serial Number ersetzen
            if elem.tag=='00181000':
                serial_number = str(elem.value)
                if serial_number in match_dict:
                    elem.value = match_dict[serial_number]
                    
            #Entferne alle PN-formatierte Tags
            if elem.VR == 'PN':
                    #pattern = re.compile(r'^export_\d+$')
                    #pattern = re.compile(r"^(bdms_|export_|suep_|hap_|pop_)\d+$")
                    if elem.tag == '00100010' and pattern.match(str(elem.value)):
                        pass
                    else:
                        Removing.replace_pn_tags_all(elem)
                    
            #Entferne Patient ID (LO)
            if elem.tag=='00100020': 
                if not pattern.match(str(elem.value)):
                    elem.value = '*removed*'
                             
            # Entfernen des gesamten Inhalts des Tags
            if elem.tag in tags_to_remove:
                if elem.VR == 'OB' or elem.VR == 'OW':
                    elem.value = b'*removed*'
                elif elem.VR in ['SH', 'LO', 'AE', 'ST', 'UT', 'LT']:
                    elem.value = '*removed*'
                elif elem.VR =='DA':
                    #Entferne Geburtstag 
                    if elem.tag=='00100030':       
                        elem.value = ''  
                    else:
                        elem.value = '*removed*'   
                #elif elem.VR == 'PN':
                #    Removing.replace_pn_tags_all(elem)
            
            # Entfernen der gewünschten Zeichenkette in Tags    
            elif elem.tag in string_in_tags_to_remove: 
                for remove_string in string_name:
                    #if elem.VR == 'PN':
                        #Removing.replace_pn_tags(elem, remove_string)
                    if elem.VR == 'OB' or elem.VR == 'OW':
                        elem.value = elem.value.replace(remove_string,b'*removed*')
                    elif elem.VR in ['SH', 'LO', 'AE', 'UT', 'ST', 'LT']:
                        elem.value = elem.value.replace(remove_string,'*removed*')
                    elif elem.VR =='DA':
                        elem.value = elem.value[:4] + '0101'
    
    
    def replace_pn_tags(elem,remove_strings):
        if hasattr(elem.value, 'given_name'):
            if remove_strings in elem.value.given_name:
                value_temp = str(elem.value)
                given_name_start = value_temp.find(elem.value.given_name)
                given_name_end = given_name_start + len(elem.value.given_name)
                value_temp = value_temp[:given_name_start] + '*removed*' + value_temp[given_name_end:]
                elem.value = value_temp
        if hasattr(elem.value, 'family_name'):
            if remove_strings in elem.value.family_name:
                value_temp = str(elem.value)
                family_name_start = value_temp.find(elem.value.family_name)
                family_name_end = family_name_start + len(elem.value.family_name)
                value_temp = value_temp[:family_name_start] + '*removed*' + value_temp[family_name_end:]
                elem.value = value_temp
        if hasattr(elem.value, 'middle_name'):
            if remove_strings in elem.value.middle_name:
                value_temp = str(elem.value)
                middle_name_start = value_temp.find(elem.value.middle_name)
                middle_name_end = middle_name_start + len(elem.value.middle_name)
                value_temp = value_temp[:middle_name_start] + '*removed*' + value_temp[middle_name_end:]
                elem.value = value_temp
        if hasattr(elem.value, 'name_suffix'):
            if remove_strings in elem.value.name_suffix:
                value_temp = str(elem.value)
                name_suffix_start = value_temp.find(elem.value.name_suffix)
                name_suffix_end = name_suffix_start + len(elem.value.name_suffix)
                value_temp = value_temp[:name_suffix_start] + '*removed*' + value_temp[name_suffix_end:]
                elem.value = value_temp
        if hasattr(elem.value, 'name_prefix'):
            if remove_strings in elem.value.name_prefix:
                value_temp = str(elem.value)
                name_prefix_start = value_temp.find(elem.value.name_prefix)
                name_prefix_end = name_prefix_start + len(elem.value.name_prefix)
                value_temp = value_temp[:name_prefix_start] + '*removed*' + value_temp[name_prefix_end:]
                elem.value = value_temp
        return elem
    

    def replace_pn_tags_all(elem):
        try:
            elem.value='*removed*' #toDo
        except Exception as e:      
            if hasattr(elem.value, 'given_name') and elem.value.given_name != '':
                value_temp = str(elem.value)
                given_name_start = value_temp.find(elem.value.given_name)
                given_name_end = given_name_start + len(elem.value.given_name)
                value_temp = value_temp[:given_name_start] + '*removed*' + value_temp[given_name_end:]
                elem.value = value_temp
            if hasattr(elem.value, 'family_name') and elem.value.family_name != '':
                value_temp = str(elem.value)
                family_name_start = value_temp.find(elem.value.family_name)
                family_name_end = family_name_start + len(elem.value.family_name)
                value_temp = value_temp[:family_name_start] + '*removed*' + value_temp[family_name_end:]
                elem.value = value_temp
            if hasattr(elem.value, 'middle_name') and elem.value.middle_name != '':
                value_temp = str(elem.value)
                middle_name_start = value_temp.find(elem.value.middle_name)
                middle_name_end = middle_name_start + len(elem.value.middle_name)
                value_temp = value_temp[:middle_name_start] + '*removed*' + value_temp[middle_name_end:]
                elem.value = value_temp
            if hasattr(elem.value, 'name_suffix') and elem.value.name_suffix != '':
                value_temp = str(elem.value)
                name_suffix_start = value_temp.find(elem.value.name_suffix)
                name_suffix_end = name_suffix_start + len(elem.value.name_suffix)
                value_temp = value_temp[:name_suffix_start] + '*removed*' + value_temp[name_suffix_end:]
                elem.value = value_temp
            if hasattr(elem.value, 'name_prefix') and elem.value.name_prefix != '':
                value_temp = str(elem.value)
                name_prefix_start = value_temp.find(elem.value.name_prefix)
                name_prefix_end = name_prefix_start + len(elem.value.name_prefix)
                value_temp = value_temp[:name_prefix_start] + '*removed*' + value_temp[name_prefix_end:]
                elem.value = value_temp
        return elem


                                    
