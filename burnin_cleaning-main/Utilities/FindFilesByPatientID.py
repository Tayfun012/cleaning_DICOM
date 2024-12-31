import os
import pydicom
import shutil
import logging


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
                    dicom = pydicom.dcmread(os.path.join(root, file),stop_before_pixels=True)
                    patient_id = dicom.PatientID  # Extract PatientID

                    # Add the file path to the dictionary under the corresponding PatientID
                    if patient_id not in dicom_dict:
                        dicom_dict[patient_id] = []
                    dicom_dict[patient_id].append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return dicom_dict

def generate_tuples(A, B, file_dict, SourceFolder, TargetFolderA, TargetFolderB):
    result_A = []
    result_B = []

    # Process keys in list A
    for key in A:
        if key in file_dict:
            for file_path in file_dict[key]:
                source_path = f"{SourceFolder}/{file_path}"
                target_path = f"{TargetFolderA}/{file_path}"
                result_A.append((source_path, target_path))

    # Process keys in list B
    for key in B:
        if key in file_dict:
            for file_path in file_dict[key]:
                source_path = f"{SourceFolder}/{file_path}"
                target_path = f"{TargetFolderB}/{file_path}"
                result_B.append((source_path, target_path))

    return result_A, result_B



# Logging einrichten
logging.basicConfig(
    filename='project_Split_6825962_out_manCleanErr1.log',  # Logdateiname
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


# Example usage:
# Replace 'your_folder_path' with the actual path to your folder containing DICOM files.
MainFolder  ="/data02/Napkon/6825962_out_manCleanErr1"
#folder_path = '/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
Substructure = 'US_1.2.840.10008.1.2.4.70'
folder_path = os.path.join(MainFolder,Substructure)#'/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'

dicom_files_by_patient = find_dicoms_by_patient(folder_path)
noImprintList   =['bdms_55280951', 'bdms_76588815', 'bdms_95748100', 'bdms_74492574', 'bdms_78583228', 'bdms_11557121', 'bdms_12421028', 'bdms_16394405', 'bdms_63226700', 'bdms_65525286', 'bdms_99748787']
ImprintList     =["bdms_12085353"]
noImprintDir="/data02/Napkon/6825962_out_manCleanErr1_clean"
ImprintDir  ="/data02/Napkon/6825962_out_manCleanErr1_imprint"

result_A, result_B = generate_tuples(noImprintList, ImprintList, dicom_files_by_patient, folder_path,  os.path.join(Substructure,noImprintDir), os.path.join(Substructure,ImprintDir))
Copypairs = result_A+result_B
copy_files_with_logging(Copypairs)

print(dicom_files_by_patient)
