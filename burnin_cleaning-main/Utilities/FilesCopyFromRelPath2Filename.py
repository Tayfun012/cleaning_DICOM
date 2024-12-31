import os
import pydicom
import shutil
import logging


# Logging einrichten
logging.basicConfig(
    filename='6825962_out_manCleanGrou1_2file.log',  # Logdateiname
    level=logging.INFO,         # Log-Level: INFO
    format='%(asctime)s - %(message)s'  # Format der Lognachrichten
)

def copy_files_with_logging(file_pairs):
    """
    Kopiert Dateien basierend auf einer Liste von Tupeln und loggt den Vorgang.
    
    :param file_pairs: Liste von Tupeln (Quelldatei, Zieldatei)
    """
    for source, destination in file_pairs:
        if os.path.exists(source):  # Prüfen, ob die Quelldatei existiert
            try:
                destination_folder = os.path.dirname(destination)
                os.makedirs(destination_folder, exist_ok=True)
                if os.path.exists(destination):
                    logging.warning(f"The file '{destination}' exists.")
                else:
                    shutil.copy2(source, destination)  # Datei kopieren
                    logging.info(f"Kopiert: {source} -> {destination}")  # Erfolgreiches Kopieren loggen
            except Exception as e:
                logging.error(f"Fehler beim Kopieren von {source} nach {destination}: {e}")
        else:
            logging.warning(f"Quelldatei existiert nicht: {source}")  # Warnung loggen


def find_dicoms_by_patient(folder_path):
    """
    Finds all DICOM files in a folder and organizes them by PatientID.

    Parameters:
        folder_path (str): The path to the folder containing DICOM files.

    Returns:
        dict: A dictionary with PatientID as keys and lists of relative file paths as values.
    """
    dicom_dict = {}

    # Walk through the directory tree
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.dcm'):  # Check if the file is a DICOM file
                file_path = os.path.relpath(os.path.join(root, file), folder_path)
                try:
                    # Read the DICOM file
                    dicom = pydicom.dcmread(os.path.join(root, file))
                    patient_id = dicom.PatientID  # Extract PatientID

                    # Add the file path to the dictionary under the corresponding PatientID
                    if patient_id not in dicom_dict:
                        dicom_dict[patient_id] = []
                    dicom_dict[patient_id].append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return dicom_dict

#MainFolder  ="/data02/Napkon/6825962_out_manCleanErr1_imprint"
MainFolder  ="/data02/Napkon/6825962_out_manCleanGrou1"
Substructure = 'US_1.2.840.10008.1.2.4.50_out_Secondary_Capture_Image_Storage'
folder_path = os.path.join(MainFolder,Substructure)#'/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
ExportFolder  = MainFolder + "_2file"



dicom_files_by_patient = find_dicoms_by_patient(folder_path)
FileList=[]
for key,value in dicom_files_by_patient.items():
    FileList=FileList+value
Copypair=[]
for Filepath in FileList:
    Relpath=os.path.join(Substructure,Filepath)
    Copypair.append((os.path.join(MainFolder,Relpath),  (os.path.join(ExportFolder,Relpath.replace("/", "__")))))
copy_files_with_logging(Copypair)
print("JEns")


