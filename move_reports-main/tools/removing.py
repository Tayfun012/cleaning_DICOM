import os
import pydicom
import shutil
from multiprocessing import Pool, cpu_count

pydicom.config.convert_wrong_length_to_UN = True

class Removing:
    #@staticmethod
    def removing_tag(input_folder, output_folder, error_folder,output_folder1):

        dicom_files = []
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".dcm"):
                    dicom_files.append((root, file))

        args = [(root, file, input_folder, output_folder, error_folder,output_folder1) for root, file in dicom_files]
        with Pool(processes=8) as pool:
            pool.map(Removing.process_dicom_file, args)
         
      
    def process_dicom_file(args):
        """Function to process a single DICOM file."""
        root, file, input_folder, output_folder, error_folder,output_folder1 = args

        try:
            # Read the DICOM file
            ds = pydicom.dcmread(os.path.join(root, file), force=True, stop_before_pixels=True)
        
            # Remove tags using the custom function
            Removing.remove_tags(ds, root, input_folder, file, output_folder, output_folder1)

        except Exception as e:
            # Handle errors and save problematic files to the error folder
            print(f"Error processing DICOM file {file}: {e}")
            relative_path = os.path.relpath(root, input_folder)
            out_path = os.path.join(error_folder, relative_path)
            os.makedirs(out_path, exist_ok=True)
            if not os.path.exists(os.path.join(out_path, file)): 
                shutil.copy(os.path.join(input_folder,relative_path, file), os.path.join(out_path, file))

        
        #--------------------------------------

        
        # for root, dirs, files in os.walk(input_folder):
        #     for file in files:
        #         if file.endswith(".dcm"):
        #             # Lesen der DICOM-Datei
        #             try:
        #                 ds = pydicom.dcmread(os.path.join(root, file), force=True, stop_before_pixels=True)
# 
        #                 # Haupttags und Subtags entfernen
        #                 Removing.remove_tags(ds,root,input_folder,file,output_folder)
        # 

    #@staticmethod
    def remove_tags(ds,root,input_folder,file,output_folder,output_folder1):
        for elem in ds:
            if elem.tag=='00080016':
                    if elem.value=='1.2.840.10008.5.1.4.1.1.7':
                    # Save DICOM File
                        relative_path = os.path.relpath(root, input_folder)
                        out_path = os.path.join(output_folder, relative_path)
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)
                        if not os.path.exists(os.path.join(out_path, file)): 
                            #ds.save_as(os.path.join(out_path, file))
                            shutil.move(os.path.join(input_folder,relative_path, file), os.path.join(out_path, file))
            elif elem.tag=='00180015':
                    if elem.value=='REPORT':
                    # Save DICOM File
                        relative_path = os.path.relpath(root, input_folder)
                        out_path = os.path.join(output_folder1, relative_path)
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)
                        if not os.path.exists(os.path.join(out_path, file)): 
                            #ds.save_as(os.path.join(out_path, file))
                            shutil.move(os.path.join(input_folder,relative_path, file), os.path.join(out_path, file))      
                            
    #@staticmethod                       
    def delete_empty_folders(input_folder):
    # Durchlaufe alle Ordner und Unterordner im Eingabeordner
        for root, dirs, files in os.walk(input_folder, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                # Wenn der Ordner leer ist, lösche ihn
                if not os.listdir(dir_path):  # Überprüft, ob der Ordner leer ist
                    os.rmdir(dir_path)  # Löscht den leeren Ordner
                    print(f'Leerer Ordner gelöscht: {dir_path}')    