import os
import shutil

def move_subfolders(input_folder, output_folder, batch_size=1000):
    # Hole alle Unterordner aus dem Inputordner
    subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    
    # Sortiere die Unterordner alphabetisch
    subfolders.sort()

    # Berechne die Gesamtzahl der Ordner
    total_subfolders = len(subfolders)

    # Gehe alle Unterordner durch in Schritten von `batch_size`
    for i in range(0, total_subfolders, batch_size):
        # Nächster Batch von Ordnern (maximal 1000)
        batch = subfolders[i:i + batch_size]
        
        # Erstelle einen neuen Zielordner im Outputordner
        batch_name = f"{os.path.basename(input_folder)}_{batch[0]}"
        batch_output_folder = os.path.join(output_folder, batch_name)
        
        # Erstelle den Batch-Ordner, falls er noch nicht existiert
        if not os.path.exists(batch_output_folder):
            os.makedirs(batch_output_folder)

        # Verschiebe alle Ordner aus dem Batch in den neuen Ordner
        for folder in batch:
            src_path = os.path.join(input_folder, folder)
            dest_path = os.path.join(batch_output_folder, folder)
            
            try:
                # Verschiebe den Ordner und seinen Inhalt
                shutil.move(src_path, dest_path)
                print(f"Ordner {folder} verschoben nach {dest_path}")
            except Exception as e:
                print(f"Fehler beim Verschieben von {folder}: {e}")

if __name__ == "__main__":
    # Definiere die Input- und Output-Ordner
    input_folder = '/data02/Napkon/6825961/'  # Ersetze dies mit deinem tatsächlichen Pfad
    output_folder = '/data02/Napkon/6825961_out/'  # Ersetze dies mit deinem tatsächlichen Pfad

    # Stelle sicher, dass der Outputordner existiert, ansonsten erstelle ihn
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Starte den Verschiebeprozess
    move_subfolders(input_folder, output_folder)
