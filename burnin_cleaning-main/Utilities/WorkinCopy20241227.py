import json
import os
from pathlib import Path
import shutil
import logging


# Logging einrichten
logging.basicConfig(
    filename='project_62.log',  # Logdateiname
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

def get_json_filenames_without_extension(directory):
    """
    Gibt eine Liste von Dateinamen ohne Erweiterung für alle JSON-Dateien im angegebenen Verzeichnis zurück.
    """
    filenames = []
    try:
        # Überprüfen, ob das Verzeichnis existiert
        if not os.path.isdir(directory):
            print(f"Das Verzeichnis '{directory}' existiert nicht.")
            return filenames
        
        # Iteriere durch die Dateien im Verzeichnis
        for file in os.listdir(directory):
            # Prüfen, ob es sich um eine JSON-Datei handelt
            if file.endswith('.json'):
                # Dateiname ohne Erweiterung hinzufügen
                filenames.append(Path(file).stem)
    except Exception as e:
        print(f"Fehler beim Zugriff auf das Verzeichnis: {e}")
    return filenames

def replace_Fileextension(file_list, old_ext, new_ext):
    """
    Replaces the file extension in a list of filenames.

    Parameters:
    - file_list: List of filenames as strings.
    - old_ext: The current extension to be replaced (e.g., 'png').
    - new_ext: The new extension to replace with (e.g., 'dcm').

    Returns:
    - A new list with updated filenames.
    """
    updated_files = []
    
    for file_name in file_list:
        # Check if the file has the old extension
        if file_name.lower().endswith(f".{old_ext}"):
            # Split the file into base name and extension
            base_name, _ = os.path.splitext(file_name)
            # Add the new extension
            updated_file = f"{base_name}.{new_ext}"
            updated_files.append(updated_file)
        else:
            # If the file doesn't match, keep it unchanged
            updated_files.append(file_name)
    
    return updated_files
def get_first_subfolder_with_pathlib(relative_path):
    path = Path(relative_path)
    # Extrahiere die Teile des Pfads
    parts = path.parts
    
    # Prüfe, ob Teile vorhanden sind und gib den ersten zurück
    if len(parts) > 0:
        return parts[0]
    else:
        return None
    
def list_files_in_subdirectories_Full(base_directory):
    """
    Listet alle Dateien in den angegebenen Unterverzeichnissen auf und gibt die relativen Pfade zurück.

    :param base_directory: Das Hauptverzeichnis, in dem sich die Unterverzeichnisse befinden.
    :param subdirectory_names: Eine Liste von Unterverzeichnisnamen.
    :return: Ein Dictionary mit Unterverzeichnisnamen als Schlüssel und Listen relativer Dateipfade als Werte.
    """
    result = {}
    subdirectory_path = base_directory
    if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
        relative_file_paths = []
        for root, _, files in os.walk(subdirectory_path):
            for file in files:
                # Berechne den relativen Pfad zur Datei
                relative_path = os.path.relpath(os.path.join(root, file), base_directory)
                relative_file_paths.append(relative_path)
        result = relative_file_paths
    else:
        # Falls das Unterverzeichnis nicht existiert
        result = None
    return result

def list_files_in_subdirectories(base_directory, subdirectory_names):
    """
    Listet alle Dateien in den angegebenen Unterverzeichnissen auf und gibt die relativen Pfade zurück.

    :param base_directory: Das Hauptverzeichnis, in dem sich die Unterverzeichnisse befinden.
    :param subdirectory_names: Eine Liste von Unterverzeichnisnamen.
    :return: Ein Dictionary mit Unterverzeichnisnamen als Schlüssel und Listen relativer Dateipfade als Werte.
    """
    result = []
    for subdirectory in subdirectory_names:
        subdirectory_path = os.path.join(base_directory, subdirectory)
        if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
            relative_file_paths = []
            for root, _, files in os.walk(subdirectory_path):
                for file in files:
                    # Berechne den relativen Pfad zur Datei
                    relative_path = os.path.relpath(os.path.join(root, file), os.path.join(base_directory,subdirectory))
                    relative_path = os.path.relpath(os.path.join(root, file), os.path.join(base_directory,get_first_subfolder_with_pathlib(subdirectory)))
                    relative_file_paths.append(relative_path)
            result+=relative_file_paths
        else:
            # Falls das Unterverzeichnis nicht existiert
            result = None
    return result

    
def mark_elements(list_a, list_b):
    # Function to compare two lists and mark elements in A based on their presence in B
    # Create a set from list B for faster lookup
    # Mark elements in A

    marked_list = {item: (True if item in list_b else False) for item in list_a}
    return marked_list

def compare_lists(list1, list2):
    # Convert lists to sets for efficient operations
    set1 = set(list1)
    set2 = set(list2)
    
    # Calculate union (all unique elements from both lists)
    union = list(set1 | set2)
    
    # Calculate exclusive elements in each list
    only_in_list1 = list(set1 - set2)
    only_in_list2 = list(set2 - set1)
    
    return {
        "union": union,
        "only_in_list1": only_in_list1,
        "only_in_list2": only_in_list2
    }


if __name__ == "__main__":
    # Benutzer nach dem Verzeichnis fragen
    
    DirectoryWithMinMaxWithJsons    = "MinMax/MinMax_Out/Napkon/"   #input("Bitte geben Sie den Pfad zu einem Verzeichnis ein: ").strip()
    DirectoryWithPNGMData           = "MinMax/PNG_Out/Napkon/"      #input("Bitte geben Sie den Pfad zu einem Verzeichnis ein: ").strip()
    
    DCMMainDir                      = "/data02/Napkon"
    DCMPackage                      = "6825962_out"
    DirectoryWithDICOMData          = os.path.join(DCMMainDir,DCMPackage)
    DirecoryOutSelectedDCMs         = os.path.join(DCMMainDir,DCMPackage+"_CTP")
    DirecoryOutNonSelectedDCMs      = os.path.join(DCMMainDir,DCMPackage+"_noCTP")
    DirecoryOutManCleanSingle       = os.path.join(DCMMainDir,DCMPackage+"_manCleanErr1")
    DirecoryOutManCleanGroup        = os.path.join(DCMMainDir,DCMPackage+"_manCleanGrou1")
    DirecoryOutCleanDCMs            = os.path.join(DCMMainDir,DCMPackage+"_Noimprints")

    #WorklistJSON                    = "/home/ipoethke/projects-ICM/BDMS/Spielwiese/Jens/XMAS2024_ExportFight/Skripts/GenerateMinMax/WorkList_62.json"
    WorklistJSON                    = "WorkList_62.json"

    if "WorklistJSON" in locals():
        with open(WorklistJSON) as f:
            WorklistSplit = json.load(f)

    # JSON-Dateinamen ohne Erweiterung abrufen
    json_filenames = get_json_filenames_without_extension(DirectoryWithMinMaxWithJsons)
    ModalityWithMinMaxImageS = json_filenames 

    
    if json_filenames:
        print("Gefundene JSON-Dateien %i: " % len(json_filenames))
        print("--> %s" % (json_filenames))
    else:
        print("Keine JSON-Dateien gefunden.")
    print("Get all DCM files in Subfolder %s " % (DirectoryWithDICOMData))
    DCMFiles=list_files_in_subdirectories(DCMMainDir, [DCMPackage])
    print("-->Found %i DCMs" % (len(DCMFiles)))
    
    print("Starting identify PNG File below Baseline %s " % (DirectoryWithPNGMData))

    ## Get JSONFiles
    PNGFiles={}
    PNGFiles['JSON']={}
    nPNGs=0
    FullDCMListsPNGSelect=[]
    for ModalityWithMinMaxImage in ModalityWithMinMaxImageS:
        print("-Getting Files for %s Folder" % (ModalityWithMinMaxImage))
        PNGFiles['JSON'][ModalityWithMinMaxImage]=list_files_in_subdirectories(DirectoryWithPNGMData,[ModalityWithMinMaxImage])
        DCMFiles =replace_Fileextension(PNGFiles['JSON'][ModalityWithMinMaxImage],'png','dcm')
        print("--> Found %i files" % len(PNGFiles['JSON'][ModalityWithMinMaxImage]))
        nPNGs+=len(PNGFiles['JSON'][ModalityWithMinMaxImage])    
    print(f"== Found {nPNGs} PNG")
    Export={}

    FullDCMListsSelect      =[]
    CheckPNGs               = mark_elements(FullDCMListsPNGSelect,DCMFiles)
    FullDCMListsSelect      +=DCMFiles
    
    Export["LabelMeJSONs"]={"Liste" : CheckPNGs, "ExportDir": DirecoryOutSelectedDCMs}


    ## Worklistbased
    
    if "WorklistJSON" in locals():
        print("Starting identify PNG File below Baseline %s by Worklist " % (DirectoryWithPNGMData))
        PNGFiles['WorkList']={}
        PNGFiles['GroupDocs']={}
        # GroupsClean        
        for GroupDocName in WorklistSplit["GroupDocs"].keys():
            for ModalityWithMinMaxImage in WorklistSplit["GroupDocs"][GroupDocName]: #Masks_Model_png 
                print("-Getting Files for %s Folder for DocID %s" % (ModalityWithMinMaxImage,GroupDocName) )
                PNGFiles['WorkList'][ModalityWithMinMaxImage]=list_files_in_subdirectories(DirectoryWithPNGMData,[ModalityWithMinMaxImage])
                DCMFiles=replace_Fileextension(PNGFiles['WorkList'][ModalityWithMinMaxImage],'png','dcm')
                print("--> Found %i files" % len(PNGFiles['WorkList'][ModalityWithMinMaxImage]))
                nPNGs+=len(PNGFiles['WorkList'][ModalityWithMinMaxImage])
            PNGFiles['GroupDocs'][GroupDocName]=[]
            for key in WorklistSplit["GroupDocs"][GroupDocName]:
                PNGFiles['GroupDocs'][GroupDocName] += PNGFiles['WorkList'][key]

            print(f"== Found {nPNGs} PNG")

        #Masks_Model_png

        FullDCMListsSelect      =[]
        WL_GroupCTPDCMs                     = replace_Fileextension(PNGFiles['GroupDocs']["Masks_Model_png"],'png','dcm') # MinMaxClean_png
        Check_GroupCleanDCMs_Group          = mark_elements(WL_GroupCTPDCMs,DCMFiles)
        FullDCMListsSelect                  +=WL_GroupCTPDCMs
        Export["LabelMeJSONs"]              ={"Liste" : WL_GroupCTPDCMs, "ExportDir": DirecoryOutSelectedDCMs}
        FullDCMListsSelect      +=DCMFiles


        WL_GroupCleanDCMs                   = replace_Fileextension(PNGFiles['GroupDocs']["MinMaxClean_png"],'png','dcm') # MinMaxClean_png
        Check_GroupCleanDCMs_Group          = mark_elements(WL_GroupCleanDCMs,DCMFiles)
        FullDCMListsSelect                  +=WL_GroupCleanDCMs
        Export["WL_GroupCleanDCMs"]         ={"Liste" : WL_GroupCleanDCMs, "ExportDir": DirecoryOutCleanDCMs}

        WL_GroupManCleanDCMs                = replace_Fileextension(PNGFiles['GroupDocs']["Manual_png"],'png','dcm') # Manual_png
        Check_GroupManCleanDCMs_Group       = mark_elements(WL_GroupManCleanDCMs,DCMFiles)
        FullDCMListsSelect                  +=WL_GroupManCleanDCMs
        Export["WL_GroupManCleanDCMs"]      ={"Liste" : WL_GroupManCleanDCMs, "ExportDir": DirecoryOutManCleanGroup}

        WL_ManualCleanDMCs_Single           =WorklistSplit["SingleSourceDocs"]["Manual_dcm"]       #Manual_dcm
        CheckManCleanDCMs_Single            = mark_elements(WL_ManualCleanDMCs_Single,DCMFiles)
        FullDCMListsSelect                  +=WL_ManualCleanDMCs_Single
        Export["ManualCleanSingles"]        ={"Liste" : WL_ManualCleanDMCs_Single, "ExportDir": DirecoryOutManCleanSingle}

        WL_CleanDMCs_Single                 =WorklistSplit["SingleSourceDocs"]["MinMaxClean_dcm"]  #MinMaxClean_dcm
        CheckManDCMs_Single                 = mark_elements(WL_CleanDMCs_Single,DCMFiles)
        FullDCMListsSelect                  +=WL_CleanDMCs_Single
        Export["WL_SingleCleanDCMs"]        ={"Liste" : WL_CleanDMCs_Single, "ExportDir": DirecoryOutCleanDCMs}



    CheckDCMs= mark_elements(DCMFiles, FullDCMListsSelect)
    print("Jens")
    copypair=[]
    for key in Export.keys(): 
        for value in Export[key]["Liste"]:
            copypair.append((os.path.join(DirectoryWithDICOMData,value),      os.path.join(Export[key]["ExportDir"],value)))
    print("Jens")
    ## Listen Erzeugen
    with open("output_Checkcopypair.txt", "w") as file:
        for tuple_item in copypair:
            # Writing each tuple as a line in the file
            file.write(f"{tuple_item}\n")

    # SourceFile TargetFile
    copy_files_with_logging(copypair)







