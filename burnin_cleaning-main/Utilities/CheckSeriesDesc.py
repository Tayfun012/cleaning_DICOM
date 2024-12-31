import os, pydicom
import logging
import shutil
import shutil, logging

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
                    try: 
                        SeriesDescription   = dicom.SeriesDescription
                    except:
                        SeriesDescription   = None

                    Modality            = dicom.Modality
                    # Add the file path to the dictionary under the corresponding PatientID
                    dicom_list.append([file_path, seriesinstanceUID, studyinstanceUID, sopinstanceUID, SeriesDescription, Modality])
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return dicom_list


MainFolder  ="/data02/Napkon/6825961_error_blacken_step1"
#folder_path = '/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
#Substructure = 'US_1.2.840.10008.1.2.4.70'
Substructure = ''
folder_path = os.path.join(MainFolder,Substructure)#'/data02/Napkon/6825962_out_manCleanErr1/US_1.2.840.10008.1.2.4.70'
#DICOMDir_unsorted = "/data02/Napkon/6825962_out_manCleanGrou1_2file/DICOMCleaner"
ExportFolderDirty  = "/data02/Napkon/6825961_error_blacken_step1_BySeries_dirty"
ExportFolderClean  = "/data02/Napkon/6825961_error_blacken_step1_BySeries_clean"

dicomOriginal   = find_dicoms_by_patient(folder_path)
for listel in dicomOriginal:
    listel[0]   = os.path.join(Substructure,listel[0])
print("Jens")
#import csv
#with open('output.csv', 'w', newline='', encoding='utf-8') as file:
#    writer = csv.writer(file)
#    writer.writerows(dicomOriginal)

CleanSeries=["rf_map",    "dMRI_dir98_AP_PhysioLog",   "dMRI_dir99_AP_PhysioLog"]
copypair=[]
for dicom in dicomOriginal:
    if dicom[4] in CleanSeries:
        copypair.append((os.path.join(folder_path,dicom[0]),os.path.join(ExportFolderClean,dicom[0])))
    else:
        copypair.append((os.path.join(folder_path,dicom[0]),os.path.join(ExportFolderDirty,dicom[0])))
copy_files_with_logging(copypair)