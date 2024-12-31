import os
import shutil

def read_and_move_files(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if "Error using File:" in line:
                # Extrahiere den Dateipfad aus der Zeile
                original_path = line.split("Error using File:")[1].strip()
                
                if os.path.exists(original_path):
                    # Ersetze '_out' durch '_error_blacken_step1' im Pfad
                    new_path = original_path.replace("_out", "_error_blacken_step1")

                    # Stelle sicher, dass der Zielordner existiert
                    new_dir = os.path.dirname(new_path)
                    os.makedirs(new_dir, exist_ok=True)

                    # Verschiebe die Datei
                    shutil.move(original_path, new_path)
                    print(f"Datei verschoben: {original_path} -> {new_path}")
                else:
                    print(f"Pfad existiert nicht: {original_path}")
    except Exception as e:
        print(f"Fehler: {e}")
        
def delete_empty_folders(input_folder):
    # Durchlaufe alle Ordner und Unterordner im Eingabeordner
    for root, dirs, files in os.walk(input_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Wenn der Ordner leer ist, lösche ihn
            if not os.listdir(dir_path):  # Überprüft, ob der Ordner leer ist
                os.rmdir(dir_path)  # Löscht den leeren Ordner
                print(f'Leerer Ordner gelöscht: {dir_path}')

# Beispielaufruf
input_error_file = "/data01/shares/projects-ICM/BDMS/Herausgabe/Programme/production/MMLabel_MinMax_Based_Labeling/MinMax/PNG_Out/Napkon/GenMinMax_Step1_error_ProNapkon-T20241225165402UTC.txt"  # Ersetze dies mit dem tatsächlichen Dateinamen
read_and_move_files(input_error_file)

# Beispiel: Gebe den Pfad des Eingabeordners an
input_project_folder = '/data02/Napkon/6825961_out' #Wenn ein Ordner bzw.Subordner leer ist dann wird es gelöscht
delete_empty_folders(input_project_folder) 

