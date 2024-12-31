import os
import shutil
from datetime import datetime

def delete_empty_folders(input_folder):
    # Durchlaufe alle Ordner und Unterordner im Eingabeordner
    for root, dirs, files in os.walk(input_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Wenn der Ordner leer ist, lösche ihn
            if not os.listdir(dir_path):  # Überprüft, ob der Ordner leer ist
                os.rmdir(dir_path)  # Löscht den leeren Ordner
                print(f'Leerer Ordner gelöscht: {dir_path}')

def extract_valid_paths(input_folder):
    """
    Extrahiert die gültigen Basispfade aus den Ordnern auf der obersten Ebene im Eingabeordner.
    """
    valid_paths = []
    for root, dirs, files in os.walk(input_folder):
        valid_paths.extend(dirs)
        break  # Nur die oberste Ebene betrachten
    return valid_paths

def log_message(log_file_path, message):
    """
    Schreibt eine Nachricht in die Logdatei. Erstellt die Datei, wenn sie nicht existiert.
    """
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Stelle sicher, dass der Ordner existiert
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as log_file:
            log_file.write("Logdatei erstellt\n")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def extract_and_move_files(error_file_path, input_folder, output_folder, log_file_path):
    try:
        # Extrahiere gültige Basispfade aus dem Eingabeordner
        valid_paths = extract_valid_paths(input_folder)
        log_message(log_file_path, f"Extrahierte gültige Pfade: {valid_paths}")

        with open(error_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if "Error using File:" in line:
                # Extrahiere den spezifischen Teil des Dateipfads
                full_path = line.split("Error using File:")[1].strip()
                
                # Überprüfe, ob der Pfad mit einem der gültigen Basispfade beginnt
                for valid_path in valid_paths:
                    if valid_path in full_path:
                        # Extrahiere den Teil ab dem gültigen Basispfad
                        start_index = full_path.find(valid_path)
                        relative_path = full_path[start_index:]

                        # Passe die Dateierweiterung an: von .png zu .dcm
                        relative_path = relative_path.replace(".png", ".dcm")

                        # Baue die vollständigen Pfade für Eingabe- und Ausgabedatei
                        source_path = os.path.join(input_folder, relative_path)
                        destination_path = os.path.join(output_folder, relative_path)

                        if os.path.exists(source_path):
                            # Stelle sicher, dass der Zielordner existiert
                            destination_dir = os.path.dirname(destination_path)
                            os.makedirs(destination_dir, exist_ok=True)

                            # Verschiebe die Datei
                            shutil.move(source_path, destination_path)
                            log_message(log_file_path, f"Datei verschoben: {source_path} -> {destination_path}")
                        else:
                            log_message(log_file_path, f"Datei nicht gefunden: {source_path}")
                        break

    except Exception as e:
        log_message(log_file_path, f"Fehler: {e}")
                
# Beispielaufruf
error_file_path = "/data01/shares/projects-ICM/BDMS/Herausgabe/Programme/production/MMLabel_MinMax_Based_Labeling/61_MinMax_61/MinMax_Out/Napkon/GenMinMax_Step1_error_ProNapkon-T20241226165646UTC.txt"
input_folder = "/data02/Napkon/6825961_out"
output_folder = "/data02/Napkon/6825961_error_blacken_step2"
log_file_path = "/data02/Napkon/Log/6825961_error_blacken_step2.log"
extract_and_move_files(error_file_path, input_folder, output_folder, log_file_path)
delete_empty_folders(input_folder)  