import os
import shutil

def move_nested_folders(input_dir, output_dir):
    # Überprüfen, ob das Zielverzeichnis existiert, ansonsten erstellen
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #i=0
    # Durchlaufen des Verzeichnisses und seiner Unterordner
    for root, dirs, _ in os.walk(input_dir):
        for dir_name in dirs:
            # Pfad des aktuellen Unterordners
            dir_path = os.path.join(root, dir_name)
            if not dir_name.startswith("_"):
                #print (dir_name)
                #i=i+1
                # Verschieben des Ordners ins Zielverzeichnis
                shutil.move(dir_path, os.path.join(output_dir, dir_name))
                print("move from %s to %s" % (dir_path, os.path.join(output_dir, dir_name)))
    #print(i)
# Pfade anpassen

input_folder = '/data02/Napkon/6825961_sortiert/'
output_folder = '/data02/Napkon/6825961'

# Funktion aufrufen
move_nested_folders(input_folder, output_folder)
