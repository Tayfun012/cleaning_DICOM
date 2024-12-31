import os, pydicom
import logging
import shutil
# Logging einrichten
logging.basicConfig(
    filename='6825962_out_manCleanGrou1_2file_cleaned.log',  # Logdateiname
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



def is_valid_dicom(file_path):
    """
    Checks if a file is a valid DICOM file, excluding DICOMDIR files.

    Args:
        file_path (str): Path to the file to check.

    Returns:
        bool: True if the file is a valid DICOM file (excluding DICOMDIR), False otherwise.
    """

    from pydicom import dcmread
    from pydicom.errors import InvalidDicomError
    from pydicom.misc import is_dicom
    
    # First, check if the file has the DICOM signature
    if not is_dicom(file_path):
        return False

    try:
        # Attempt to read the DICOM dataset
        ds = dcmread(file_path, stop_before_pixels=True)
        
        # Exclude DICOMDIR files by checking the Media Storage SOP Class UID
        if hasattr(ds.file_meta, "MediaStorageSOPClassUID") and ds.file_meta.MediaStorageSOPClassUID == "1.2.840.10008.1.3.10":
            return False  # It's a DICOMDIR file
        
        return True  # Valid DICOM file
    except InvalidDicomError:
        return False  # Not a valid DICOM file


def find_dicoms_by_patient(folder_path):
    """
    Finds all DICOM files in a folder and organizes them by PatientID.

    Parameters:
        folder_path (str): The path to the folder containing DICOM files.

    Returns:
        dict: A dictionary with PatientID as keys and lists of relative file paths as values.
    """
    dicom_list = [] 

    # Walk through the directory tree
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path_full = os.path.join(root, file)
            if is_valid_dicom(file_path_full):  # Check if the file is a DICOM file
                try:
                    # Read the DICOM file
                    file_path = os.path.relpath(os.path.join(root, file), folder_path)
                    dicom = pydicom.dcmread(os.path.join(root, file),stop_before_pixels=True)
                    #patient_id          = dicom.PatientID  # Extract PatientID
                    seriesinstanceUID   = dicom.SeriesInstanceUID
                    studyinstanceUID    = dicom.StudyInstanceUID
                    sopinstanceUID      = dicom.SOPInstanceUID
                    # Add the file path to the dictionary under the corresponding PatientID
                    dicom_list.append([file_path, seriesinstanceUID, studyinstanceUID, sopinstanceUID])
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return dicom_list

def compare_lists_by_suffix(list1, list2):
    """
    Compares two lists of 4-element sublists by the last 3 elements of each sublist.
    Returns a list of tuples containing matching sublists from both lists.

    :param list1: First list of 4-element sublists
    :param list2: Second list of 4-element sublists
    :return: List of tuples with matching sublists
    """
    matches = []
    for sublist1 in list1:
        for sublist2 in list2:
            # Compare the last three elements of each sublist
            if sublist1[1:4] == sublist2[1:4]:
                matches.append((sublist1, sublist2))
    return matches


MainFolder  ="/data02/Napkon/6825962_out_manCleanGrou1"
#folder_path = '/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
#Substructure = 'US_1.2.840.10008.1.2.4.70'
Substructure = ''
folder_path = os.path.join(MainFolder,Substructure)#'/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
DICOMDir_unsorted = "/data02/Napkon/6825962_out_manCleanGrou1_2file/DICOMCleaner"
ExportFolder  = "/data02/Napkon/6825962_out_manCleanGrou1_2file_clean"

dicomOriginal   = find_dicoms_by_patient(folder_path)
for listel in dicomOriginal:
    listel[0]   = os.path.join(Substructure,listel[0])
DICOM_unsorted  = find_dicoms_by_patient(DICOMDir_unsorted)
matches= compare_lists_by_suffix(dicomOriginal, DICOM_unsorted )

FileList=[]

Copypair=[]
for Filepath in matches:
    Copypair.append((os.path.join(DICOMDir_unsorted,Filepath[1][0]), os.path.join(ExportFolder,Filepath[0][0])))
copy_files_with_logging(Copypair)

print("JEns")