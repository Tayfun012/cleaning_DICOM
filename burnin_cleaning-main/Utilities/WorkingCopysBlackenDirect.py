import os, json
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
                shutil.copy2(source, destination)  # Datei kopieren
                logging.info(f"Kopiert: {source} -> {destination}")  # Erfolgreiches Kopieren loggen
            except Exception as e:
                logging.error(f"Fehler beim Kopieren von {source} nach {destination}: {e}")
        else:
            logging.warning(f"Quelldatei existiert nicht: {source}")  # Warnung loggen

def check_path_type(path):
    """
    Prüft, ob der gegebene Pfad auf eine Datei, ein Verzeichnis oder nichts verweist.

    :param path: Der zu überprüfende Pfad
    :return: String, der den Typ des Pfads beschreibt ("Datei", "Verzeichnis", "Weder Datei noch Verzeichnis")
    """
    if os.path.isfile(path):
        return "Datei"
    elif os.path.isdir(path):
        return "Verzeichnis"
    else:
        return "Weder Datei noch Verzeichnis"
def list_files_by_extension(directory, extension):
    """
    Listet alle Dateien in den Unterverzeichnissen eines Verzeichnisses auf und filtert nach Dateierweiterung.

    :param directory: Das Verzeichnis, in dem gesucht werden soll
    :param extension: Die Dateierweiterung, nach der gefiltert werden soll (z. B. ".txt")
    :return: Liste der relativen Pfade zu den Dateien mit der angegebenen Erweiterung
    """
    matching_files = []
    for root, _, files in os.walk(directory):  # Durchlaufe alle Unterverzeichnisse
        for file in files:
            if file.endswith(extension):  # Prüfe auf die gewünschte Dateierweiterung
                relative_path = os.path.relpath(os.path.join(root, file), directory)  # Relativen Pfad berechnen
                matching_files.append(os.path.join(root, file))
    return matching_files

import os

def get_lowercase_extension(file_path):
    """
    Extrahiert die Dateierweiterung eines gegebenen Pfads und gibt sie in Kleinbuchstaben zurück.

    :param file_path: Der Dateipfad
    :return: Die Dateierweiterung in Kleinbuchstaben (z. B. ".txt")
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def Dateiliste(SourceFolder, PathValue,FileExt):
    Dateiliste=[]
    InPath=os.path.join(SourceFolder,PathValue)
    Check=check_path_type(InPath)
    if  Check == "Datei":
        Dateiliste.append(InPath)
    if Check == "Verzeichnis" and PathValue is not '':
        Dateiliste.extend(list_files_by_extension(InPath,FileExt))
    if Check == "Weder Datei noch Verzeichnis":
        logging.warning(f"Dateiliste: Angabe ist nicht für eine Datei verarbeitbar {PathValue} mit {SourceFolder}")  # Warnung loggen
        logging.info(f"Dateiliste: Für {PathValue} wurden {len(Dateiliste)} Dateien identifiziert")
    return Dateiliste

def CreateWorkItemsFromSource(SourceFolder, TargetFolder, PathValue):
    WorkList=[]
    # Step 1 get all Files
    Dateiliste=[]
    if check_path_type(PathValue) == "Datei":
        Dateiliste.append(PathValue)
    if check_path_type(PathValue) == "Verzeichnis":
        print("Jens")
        Dateiliste.append(list_files_by_extension(PathValue, '.png'))
        Dateiliste.append(list_files_by_extension(PathValue, '.dcm'))
    if check_path_type(PathValue) == "Weder Datei noch Verzeichnis":
        logging.warning(f"WL: Angabe ist nicht für eine Worlisterstellung verarbeitbar.  {PathValue}")  # Warnung loggen
    # Step 2 if File DCM or dcm --> Direct Copy: if png --> retrieve the dcm file in source and then create copy




    return WorkList
def replace_base_path(full_path, old_base, new_base):
        from pathlib import Path
        """
        Replace the base path of a full path with a new root path.

        :param full_path: The original full path as a string
        :param old_base: The base part of the path to be replaced
        :param new_base: The new root path to replace the old base
        :return: A new path with the base replaced
        """
        full_path = Path(full_path)
        old_base = Path(old_base)
        new_base = Path(new_base)

        # Ensure the full_path starts with old_base
        if not str(full_path).startswith(str(old_base)):
            raise ValueError(f"The full path does not start with the specified old base: {old_base}")

        # Get the relative part of the path after old_base
        relative_part = full_path.relative_to(old_base)

        # Combine the new base with the relative part
        new_path = new_base / relative_part

        return str(new_path)

def TransformPNGpathToDCM(BaseDir, filelist, Targetpath, SourceExtension, Targetextension):
    

    def change_file_extension(file_path, new_extension):
        from pathlib import Path
        """
        Replace the file extension of a given file path with a new extension.

        :param file_path: The original file path as a string
        :param new_extension: The new extension (without the dot) as a string
        :return: The updated file path as a string
        """
        path = Path(file_path)
        # Use with_suffix to replace the file extension
        new_file_path = path.with_suffix("." + new_extension)
        return str(new_file_path)
    
    def check_file_exists(file_path):
        """
        Überprüft, ob der angegebene Dateipfad zu einer existierenden Datei führt.

        :param file_path: Der zu überprüfende Dateipfad.
        :return: True, wenn die Datei existiert, andernfalls False.
        """
        return os.path.isfile(file_path)
    
    
    DCMFiles=[]
    for file in filelist:
        #Fullpath=os.path.join(BaseDir, filelist[0])
        tempfilename = replace_base_path(file,BaseDir,Targetpath)
        tempfilename = change_file_extension(tempfilename,'dcm')
        if check_file_exists(tempfilename):
            DCMFiles.append(tempfilename)
        else:
            logging.warning(f"PNG2DMC: DCM Datei exisitert nicht: {file}")  # Warnung loggen
    return DCMFiles


def get_first_subdirectory(relative_path):
    from pathlib import Path 
    """
    Gibt das erste Unterverzeichnis eines relativen Pfades zurück.

    :param relative_path: Der relative Pfad als String.
    :return: Das erste Unterverzeichnis als String oder None, wenn kein Unterverzeichnis existiert.
    """
    path = Path(relative_path)
    return path.parts[0] if path.parts else None





Project="62"
WorklistAgenda_File="GenerateMinMax/WorkList_%s.json" % (Project)
with open(WorklistAgenda_File, 'r') as file:
    WorklistAgenda = json.load(file)
ProjectSources  ={"62": "/data02/Napkon/6825962_out" }
PNGSource       ={"62": "./GenerateMinMax/MinMax/PNG_out/Napkon" }
ProjectTarget   ={"62": "/data02/Napkon/6825962_out_%s"}
SourceFolder    =ProjectSources[Project]


# GroupDocs/MinMaxClean
# GroupDocs/Masks_Model
# GroupDocs/Manual
# SingleDocs/ErrorsGen01
# SingleDocs/Manual
# SingleDocs/MinMaxClean
# SingleDocs/ErrorsGen02

WorkingCode={ 
    "MinMaxClean_png"   : "ImgClean", 
    "MinMaxClean_dcm"   : "ImgClean", 
    "Manual_png"        : "ImgDirtyMan",
    "Manual_dcm"        : "ImgDirtyMan",
    "Masks_Model_png"   : "ImgDirtyInCTP",
    "Masks_Model_dcm"   : "ImgDirtyInCTP",
    "ErrorsGen02_png"   : "ImgErrorGen2ImgSize", 
    "ErrorsGen02_dcm"   : "ImgErrorGen2ImgSize", 
    "ErrorsGen01_png"   : "ImgError_ManCheck",
    "ErrorsGen01_dcm"   : "ImgError_ManCheck"
      }

DirectCopy={ 
    "MinMaxClean_png"   : False, 
    "MinMaxClean_dcm"   : True, 
    "Manual_png"        : False,
    "Manual_dcm"        : True,
    "Masks_Model_png"   : False,
    "Masks_Model_dcm"   : True,
    "ErrorsGen02_png"   : False, 
    "ErrorsGen02_dcm"   : True, 
    "ErrorsGen01_png"   : False,
    "ErrorsGen01_dcm"   : True }

WorkList=[]


FileList=[]
for Subkey, ValueList in WorklistAgenda["SingleSourceDocs"].items():
    DCM_List=[]
    for Value in ValueList:
        if DirectCopy[Subkey]:
            DCM_List=Dateiliste("/data02/Napkon/68259%s_out" % (Project), Value,'.dcm')
        else:
            PNG_List=Dateiliste(PNGSource[Project], Value,'.png')
            DCM_List=TransformPNGpathToDCM(os.path.join(PNGSource[Project],get_first_subdirectory(Value)),PNG_List,"/data02/Napkon/68259%s_out" % (Project),'.png','dcm')
        FileList.extend(DCM_List)
    for DCMFile in DCM_List:
            WorkList.append((DCMFile,replace_base_path(DCMFile, SourceFolder, ProjectTarget[Project] % WorkingCode[Subkey])))

for Subkey, ValueList in WorklistAgenda["GroupDocs"].items():
    DCM_List=[]
    for Value in ValueList:
        if DirectCopy[Subkey]:
            DCM_List=Dateiliste("/data02/Napkon/68259%s_out" % (Project), Value,'.dcm')
        else:
            PNG_List=Dateiliste(PNGSource[Project], Value,'.png')
            DCM_List=TransformPNGpathToDCM(os.path.join(PNGSource[Project],get_first_subdirectory(Value)),PNG_List,"/data02/Napkon/68259%s_out" % (Project),'.png','dcm')
        FileList.extend(DCM_List)
        for DCMFile in DCM_List:
            WorkList.append((DCMFile,replace_base_path(DCMFile, SourceFolder, ProjectTarget[Project] % WorkingCode[Subkey])))
        #WorkList.append(CreateWorkItemsFromSource("/data02/Napkon/68259%s_out" % (Project),"/data02/Napkon/68259%s_%s" % (Project, WorkingCode[Subkey]), Value))
        print("Worklist Length: %i" % (len(WorkList)))

# Beispielhafte Nutzung
file_pairs = [
    ("quelle1.txt", "ziel1.txt"),
    ("quelle2.txt", "ziel2.txt")
]

#copy_files_with_logging(file_pairs)




