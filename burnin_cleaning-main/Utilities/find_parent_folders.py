import os

def find_parent_folders(base_dir, target_folder_names):
    """
    Sucht in einem Verzeichnis (base_dir) nach bestimmten Ordnernamen (target_folder_names) in Ebene 2
    und gibt die zugehörigen Ordnernamen aus Ebene 1 zurück.

    :param base_dir: Basisverzeichnis, das durchsucht wird
    :param target_folder_names: Liste von Ordnernamen, die gesucht werden
    :return: Dictionary mit {gefundenes_Ebene_2_Ordnername: [entsprechende_Ebene_1_Ordnernamen]}
    """
    result = {}

    for level1_folder in os.listdir(base_dir):
        level1_path = os.path.join(base_dir, level1_folder)

        if os.path.isdir(level1_path):  # Ebene 1 überprüfen
            for level2_folder in os.listdir(level1_path):
                level2_path = os.path.join(level1_path, level2_folder)

                if os.path.isdir(level2_path) and level2_folder in target_folder_names:
                    if level2_folder not in result:
                        result[level2_folder] = []
                    result[level2_folder].append(level1_folder)

    return result



def save_results_to_file(results, file_path):
    """
    Speichert die Ergebnisse in einer Datei, wobei jeder Eintrag untereinander geschrieben wird.

    :param results: Dictionary mit {Ordnername: [Liste von Ebene-1-Ordnernamen]}
    :param file_path: Pfad zur Datei, in die geschrieben werden soll
    """
    with open(file_path, 'w') as file:
        for level2, level1_list in results.items():
            file.write(f"Gefundener Ordner: {level2}\n")
            for level1 in level1_list:
                file.write(f"{level1}\n")
            file.write("\n")  # Leerzeile zwischen Einträgen

# Beispielverwendung
if __name__ == "__main__":
    # Basisverzeichnis, das durchsucht werden soll
    base_directory = r"X:\\BDMS\\Herausgabe\\Programme\\production\\MMLabel_MinMax_Based_Labeling\\MinMax\\PNG_Out\\Napkon"

    # Liste der Zielordnernamen in Ebene 2
    target_folders = ["CT_1.2.840.10008.1.2"]
    #target_folders = ["Zielordner1", "Zielordner2"]

    # Funktion aufrufen
    matches = find_parent_folders(base_directory, target_folders)

    # Ergebnisse speichern
    output_file = r"X:\\BDMS\\Herausgabe\\Programme\\production\\MMLabel_MinMax_Based_Labeling\\MinMax\\PNG_Out\\CT_1.2.840.10008.1.2.txt"
    save_results_to_file(matches, output_file)

    # Ergebnisse ausgeben
    print(f"Ergebnisse wurden in {output_file} gespeichert.")
