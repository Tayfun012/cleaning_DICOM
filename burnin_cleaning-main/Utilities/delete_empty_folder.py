import os

def delete_empty_folders(input_folder):
    # Durchlaufe alle Ordner und Unterordner im Eingabeordner
    for root, dirs, files in os.walk(input_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Wenn der Ordner leer ist, lösche ihn
            if not os.listdir(dir_path):  # Überprüft, ob der Ordner leer ist
                os.rmdir(dir_path)  # Löscht den leeren Ordner
                print(f'Leerer Ordner gelöscht: {dir_path}')

# Beispiel: Gebe den Pfad des Eingabeordners an
input_folder = '/data02/Napkon/6825960_out'
delete_empty_folders(input_folder)